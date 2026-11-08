import { configured } from '../lib/store.js';
export default function handler(req,res) {
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='GET') return res.status(405).json({ok:false,error:'Use GET'});
  const ready=configured();
  return res.status(ready?200:503).json({
    ok:ready,service:'fire-inbox',protocol:'LC1',storage:ready?'configured':'missing',
    routes:['GET /api/messages','POST /api/messages','GET /api/send?q=&id=',
      'GET /api/messages/status?id=&done=','WSS /api/ws']
  });
}
