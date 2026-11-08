import { InputError, normalizeMessage } from '../lib/protocol.js';
import { listMessages, saveMessage, configured } from '../lib/store.js';

export default async function handler(req,res) {
  res.setHeader('Cache-Control','no-store');
  if (!configured()) return res.status(503).json({ok:false,error:'Inbox storage has not been provisioned'});
  try {
    if(req.method==='GET') {
      const u=new URL(req.url,'https://localhost');
      const to=u.searchParams.get('to')||undefined;
      const after=u.searchParams.get('after')||undefined;
      let limit=Number(u.searchParams.get('limit')||50);
      if(!Number.isInteger(limit)||limit<1||limit>100) throw new InputError('limit must be 1–100');
      if(to && !/^(human|agent|device|project):[a-z0-9][a-z0-9._/-]{0,63}$/.test(to)) throw new InputError('Invalid recipient');
      const messages=await listMessages({recipient:to,after,limit});
      return res.status(200).json({ok:true,messages,count:messages.length});
    }
    if(req.method==='POST') {
      let body=req.body;
      if(typeof body==='string') {
        const type=req.headers['content-type']||'';
        if(type.includes('application/json')) body=JSON.parse(body);
        else if(type.includes('application/x-www-form-urlencoded')) {
          const params=new URLSearchParams(body);
          body={message:params.get('message')||params.get('q')||'',id:params.get('id')||undefined};
        } else body={text:body};
      }
      const input=normalizeMessage(body);
      const saved=await saveMessage(input);
      return res.status(saved.created?201:200).json({ok:true,saved:true,id:input.id,message:saved.message,created:saved.created});
    }
    res.setHeader('Allow','GET, POST');
    return res.status(405).json({ok:false,error:'Method not allowed'});
  }catch(e){
    console.error('messages API',e?.status||500,e?.message);
    return res.status(e instanceof InputError?e.status:500)
      .json({ok:false,error:e instanceof InputError?e.message:'Storage unavailable'});
  }
}
