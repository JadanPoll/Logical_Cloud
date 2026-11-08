import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source=fs.readFileSync(new URL('../public/identity.js',import.meta.url),'utf8');
function harness(){
  const backing=new Map();
  const storage={
    getItem:key=>backing.get(key)||null,
    setItem:(key,value)=>backing.set(key,value)
  };
  const context={
    crypto:{getRandomValues:buf=>{buf.set([4,10,19,120,61,32]);return buf;}},
    Uint8Array,Array,JSON,String,Error,
  };
  vm.runInNewContext(source,context);
  return {storage,api:context.FireInboxIdentity,backing};
}

test('browser identity persists across reloads and renames without changing address',()=>{
  const {storage,api}=harness();
  const first=api.load(storage,null);
  assert.equal(first.id,'device:browser-040a13783d20');
  assert.equal(first.label,'This browser');
  const renamed=api.rename(storage,first,'Windows - Alex');
  const again=api.load(storage,null);
  assert.equal(renamed.id,first.id);
  assert.equal(again.id,first.id);
  assert.equal(again.label,'Windows - Alex');
  assert.equal(again.persistent,true);
});

test('Fire TV-provided native sender identity wins and survives visits',()=>{
  const {storage,api}=harness();
  api.load(storage,null);
  const seeded=api.load(storage,'device:fire-tv-0123456789ab');
  assert.equal(seeded.id,'device:fire-tv-0123456789ab');
  assert.equal(seeded.label,'Fire TV');
  const named=api.rename(storage,seeded,'Bedroom Fire TV');
  const reopened=api.load(storage,'device:fire-tv-0123456789ab');
  assert.equal(reopened.id,seeded.id);
  assert.equal(reopened.label,named.label);
  assert.equal(reopened.persistent,true);
});

test('spoofed URL from parameter does not silently replace persisted address',()=>{
  const {storage,api}=harness();
  const initial=api.load(storage,null);
  assert.equal(api.load(storage,'agent:owner').id,initial.id);
  assert.equal(api.load(storage,'device:fire-tv-../fake').id,initial.id);
});

test('blocked storage does not crash the app, but reports missing persistence',()=>{
  const {api}=harness();
  const blocked={getItem(){throw Error('blocked');},setItem(){throw Error('blocked');}};
  const result=api.load(blocked,null);
  assert.equal(result.persistent,false);
  assert.equal(result.id,'device:browser-040a13783d20');
  assert.equal(api.rename(blocked,result,'Living Room').persistent,false);
});
