import { normalizeMessage, InputError } from '../lib/protocol.js';
import { configured, saveMessage } from '../lib/store.js';

export default async function handler(req,res) {
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='GET') return res.status(405).json({ok:false,error:'Use GET'});
  if(!configured()) return res.status(503).json({ok:false,error:'Inbox storage unavailable'});
  try {
    const url=new URL(req.url,'https://localhost');
    const input=normalizeMessage({
      text:url.searchParams.get('q'),
      id:url.searchParams.get('id'),
      from:url.searchParams.get('from')||undefined,
      from_label:url.searchParams.get('from_label')||undefined
    });
    const saved=await saveMessage(input);
    return res.status(200).json({
      ok:true,saved:true,id:input.id,message:{id:input.id},created:saved.created
    });
  }catch(e) {
    console.error('send API',e?.status||500,e?.message);
    return res.status(e instanceof InputError?e.status:500)
      .json({ok:false,error:e instanceof InputError?e.message:'Storage unavailable'});
  }
}
