import { createServer } from 'node:http';
import { WebSocketServer, WebSocket } from 'ws';
import { normalizeMessage, InputError } from '../lib/protocol.js';
import { configured, listMessages, saveMessage } from '../lib/store.js';

// A connection is pinned to one Vercel Function. The Blob store, not
// process memory, owns history. Each socket polls it for cross-instance
// catch-up. Later we can replace this narrow polling adapter with Redis.
const server=createServer((req,res)=>{
  res.writeHead(426,{'Content-Type':'application/json','Cache-Control':'no-store'});
  res.end(JSON.stringify({ok:false,error:'WebSocket upgrade required; otherwise use HTTPS /api/messages'}));
});
const wss=new WebSocketServer({server,path:'/api/ws'});

function send(ws,value) {
  if(ws.readyState===WebSocket.OPEN) ws.send(JSON.stringify(value));
}
function deliver(ws,msg) {
  if(ws.recipient && msg.to!==ws.recipient) return;
  if(ws.seen.has(msg.id)) return;
  ws.seen.add(msg.id);
  if(ws.seen.size>300)ws.seen=new Set([...ws.seen].slice(-200));
  send(ws,{type:'message',message:msg});
}
async function catchup(ws) {
  if(!ws.recipient || ws.fetching || ws.readyState!==WebSocket.OPEN) return;
  ws.fetching=true;
  try {
    const recent=await listMessages({recipient:ws.recipient,limit:35});
    for (const msg of recent.slice().reverse())deliver(ws,msg);
  } catch(e) {
    console.error('WSS history catchup',e?.message);
    send(ws,{type:'error',error:'History unavailable; use HTTPS recovery'});
  } finally {ws.fetching=false;}
}
wss.on('connection',ws=>{
  if(!configured()) {
    send(ws,{type:'error',error:'Storage is not configured'});
    ws.close(1013,'Storage unavailable');
    return;
  }
  if(wss.clients.size>40) {
    ws.close(1013,'Server busy; use HTTPS polling');
    return;
  }
  ws.recipient=null;
  ws.seen=new Set();
  ws.fetching=false;
  ws.lastSendAt=0;
  send(ws,{type:'hello',protocol:'LC1',durable_recovery:'/api/messages',max_message_length:1600});

  const refresh=setInterval(()=>{void catchup(ws);},12000);
  ws.on('close',()=>clearInterval(refresh));
  ws.on('error',()=>clearInterval(refresh));
  ws.on('message', async frame=>{
    if(frame.length>4096) {send(ws,{type:'error',error:'Frame too large'});return;}
    let data;
    try {data=JSON.parse(frame.toString('utf8'));} catch {
      send(ws,{type:'error',error:'Expected JSON'});return;
    }
    if(data?.type==='subscribe') {
      const to=data.to;
      if(typeof to!=='string' || !/^(human|agent|device|project):[a-z0-9][a-z0-9._/-]{0,63}$/.test(to)) {
        send(ws,{type:'error',error:'Invalid recipient'});return;
      }
      ws.recipient=to;
      ws.seen=new Set();
      send(ws,{type:'subscribed',to});
      void catchup(ws);
      return;
    }
    if(data?.type==='ping') {send(ws,{type:'pong'});return;}
    if(data?.type!=='send') {send(ws,{type:'error',error:'Unknown action'});return;}
    if(Date.now()-ws.lastSendAt<2000) {
      send(ws,{type:'error',error:'Please allow two seconds between sends'});return;
    }
    ws.lastSendAt=Date.now();
    try {
      const input=normalizeMessage(data.message);
      const saved=await saveMessage(input);
      send(ws,{type:'ack',id:input.id,ok:true,created:saved.created});
      if(saved.created)for(const client of wss.clients)deliver(client,saved.message);
    } catch(e) {
      console.error('WSS send',e?.status||500,e?.message);
      send(ws,{type:'error',id:data?.message?.id||null,
        error:e instanceof InputError?e.message:'Save failed; reconcile ID over HTTPS'});
    }
  });
});
export default server;
