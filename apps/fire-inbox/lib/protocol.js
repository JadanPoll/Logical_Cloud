import { randomUUID } from 'node:crypto';

export const MESSAGE_KINDS = new Set([
  'question','opinion','proposal','decision','request','progress',
  'result','observation','presence','message'
]);
const ADDRESS = /^(human|agent|device|project):[a-z0-9][a-z0-9._/-]{0,63}$/;
const ID = /^[a-zA-Z0-9._-]{8,96}$/;
const TEXT_LIMIT = 1600;

export class InputError extends Error {
  constructor(message, status=400) { super(message); this.status=status; }
}
export function validId(id) {
  if (typeof id !== 'string' || !ID.test(id)) throw new InputError('Invalid message ID');
  return id;
}
export function optionalAddress(value, fallback) {
  if (value == null || value === '') return fallback;
  if (typeof value !== 'string' || !ADDRESS.test(value)) throw new InputError('Invalid participant address');
  return value;
}
export function parseWire(raw) {
  if (typeof raw !== 'string' || !raw.startsWith('[LC1 ')) return null;
  const marker=raw.indexOf(']\n');
  if (marker < 6 || marker > 1150) return null;
  try {
    const meta=JSON.parse(raw.slice(5,marker));
    if (!meta || typeof meta !== 'object' || !ADDRESS.test(meta.from) ||
        !ADDRESS.test(meta.to) || !MESSAGE_KINDS.has(meta.kind)) return null;
    if (typeof meta.id !== 'string' || !ID.test(meta.id)) return null;
    return { ...meta, body: raw.slice(marker+2) };
  } catch { return null; }
}
export function normalizeMessage(value, suppliedId=null) {
  const obj=typeof value === 'string' ? {text:value} : value;
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) throw new InputError('Message must be text or JSON object');
  const raw=obj.message ?? obj.text ?? obj.q;
  if (typeof raw !== 'string' || !raw.trim() || raw.length>TEXT_LIMIT || /\u0000/.test(raw)) {
    throw new InputError('Message must contain 1–1600 characters');
  }
  const wrapped=parseWire(raw);
  const id=validId(suppliedId || obj.id || wrapped?.id || randomUUID());
  if (wrapped && wrapped.id!==id) throw new InputError('LC1 header ID does not match request ID');
  const kind=obj.kind || wrapped?.kind || 'message';
  if (!MESSAGE_KINDS.has(kind)) throw new InputError('Unknown message kind');
  const from=optionalAddress(obj.from || wrapped?.from, 'human:anonymous');
  const to=optionalAddress(obj.to || wrapped?.to, 'human:owner');
  const project=obj.project || wrapped?.project || '';
  if (typeof project!=='string' || project.length>120 || /[\r\n\u0000]/.test(project)) {
    throw new InputError('Invalid project');
  }
  const reply_to=obj.reply_to || wrapped?.reply_to || null;
  if (reply_to!==null) validId(reply_to);
  const refs=obj.refs || wrapped?.refs || [];
  if (!Array.isArray(refs) || refs.length>3 || refs.some(r=>
    typeof r!=='string' || r.length>180 || !(
      r.startsWith('https://github.com/') || /^sha256:[a-f0-9]{64}$/.test(r)))) {
    throw new InputError('Refs must be GitHub URLs or sha256 hashes');
  }
  return {
    id, message:raw, text:wrapped?wrapped.body:raw,
    from, to, kind, project, reply_to, refs,
    created_at:wrapped?.created_at || new Date().toISOString(),
    stored_at:new Date().toISOString(), done:false, schema_version:1
  };
}
export function publicMessage(m) {
  return {
    id:m.id, message:m.message, text:m.text, body:m.text,
    from:m.from,to:m.to,kind:m.kind,project:m.project,
    reply_to:m.reply_to,refs:m.refs,created_at:m.created_at,
    timestamp:m.stored_at,done:!!m.done
  };
}
export function parseDone(value) {
  if (value==='1' || value==='true') return true;
  if (value==='0' || value==='false') return false;
  throw new InputError('done must be 1 or 0');
}
