import { get, list, put } from '@vercel/blob';
import { InputError, publicMessage } from './protocol.js';

const ACCESS='private';
const prefix='inbox-v1/';
const messagePath=id=>prefix+'messages/'+id+'.json';
const statusPath=id=>prefix+'status/'+id+'.json';

async function read(path) {
  const result=await get(path,{access:ACCESS,useCache:false});
  if (!result || result.statusCode===404) return null;
  if (result.statusCode!==200) throw new Error('Storage read failed: '+result.statusCode);
  return JSON.parse(await new Response(result.stream).text());
}
export function configured() {
  return Boolean(process.env.BLOB_READ_WRITE_TOKEN || process.env.BLOB_STORE_ID);
}
export async function getMessage(id) {
  return read(messagePath(id));
}
export async function saveMessage(msg) {
  const old=await getMessage(msg.id);
  if (old) {
    if (old.message!==msg.message || old.from!==msg.from ||
        old.to!==msg.to || old.kind!==msg.kind) {
      throw new InputError('Message ID was already used with different content',409);
    }
    return {message:publicMessage(old),created:false};
  }
  try {
    await put(messagePath(msg.id),JSON.stringify(msg),
      {access:ACCESS,addRandomSuffix:false,contentType:'application/json'});
    return {message:publicMessage(msg),created:true};
  } catch(e) {
    // Concurrent duplicate sends can both observe absence; the immutable
    // pathname provides the only authoritative winner.
    const winner=await getMessage(msg.id);
    if (winner) {
      if (winner.message===msg.message && winner.from===msg.from &&
          winner.to===msg.to && winner.kind===msg.kind) {
        return {message:publicMessage(winner),created:false};
      }
      throw new InputError('Message ID conflict',409);
    }
    throw e;
  }
}
export async function setStatus(id, done) {
  const msg=await getMessage(id);
  if (!msg) throw new InputError('Message not found',404);
  const state={id,done,updated_at:new Date().toISOString()};
  await put(statusPath(id),JSON.stringify(state),
    {access:ACCESS,allowOverwrite:true,contentType:'application/json'});
  return state;
}
async function listMessageMetadata() {
  const blobs=[];
  let cursor;
  for(let page=0;page<3;page++) {
    const result=await list({prefix:prefix+'messages/',limit:1000,cursor});
    blobs.push(...result.blobs);
    if(!result.hasMore || !result.cursor) break;
    cursor=result.cursor;
  }
  return blobs;
}
export async function listMessages({recipient,after,limit=50}={}) {
  const meta=await listMessageMetadata();
  meta.sort((a,b)=>new Date(b.uploadedAt)-new Date(a.uploadedAt));
  const since=after?Date.parse(after):null;
  if(after && !Number.isFinite(since)) throw new InputError('Invalid after timestamp');
  const filtered=meta.filter(b=>since===null || Date.parse(b.uploadedAt)>since).slice(0,Math.min(100,Math.max(limit*3,limit)));
  // Storage work is bounded by request limit and does not read unlimited history.
  const rows=[];
  for(let i=0;i<filtered.length;i+=10) {
    const chunk=await Promise.all(filtered.slice(i,i+10).map(b=>read(b.pathname)));
    rows.push(...chunk.filter(Boolean));
  }
  const matching=rows.filter(m=>!recipient || m.to===recipient).slice(0,limit);
  // Status is a separate key, so editing a checkmark never overwrites
  // the durable immutable message record.
  const results=[];
  for(let i=0;i<matching.length;i+=10) {
    const chunk=await Promise.all(matching.slice(i,i+10).map(async m=>{
      const status=await read(statusPath(m.id));
      return publicMessage({...m,done:status?status.done:m.done});
    }));
    results.push(...chunk);
  }
  return results;
}
