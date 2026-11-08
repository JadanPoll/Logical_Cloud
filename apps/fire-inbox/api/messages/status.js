import { InputError, validId, parseDone } from '../../lib/protocol.js';
import { configured, setStatus } from '../../lib/store.js';

export default async function handler(req,res) {
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='GET') return res.status(405).json({ok:false,error:'Use GET'});
  if(!configured()) return res.status(503).json({ok:false,error:'Storage unavailable'});
  try {
    const url=new URL(req.url,'https://localhost');
    const id=validId(url.searchParams.get('id'));
    const done=parseDone(url.searchParams.get('done'));
    const result=await setStatus(id,done);
    return res.status(200).json({ok:true,...result});
  }catch(e) {
    console.error('status API',e?.status||500,e?.message);
    return res.status(e instanceof InputError?e.status:500)
      .json({ok:false,error:e instanceof InputError?e.message:'Storage unavailable'});
  }
}
