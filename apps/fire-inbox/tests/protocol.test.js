import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeMessage, parseWire, publicMessage, parseDone, InputError } from '../lib/protocol.js';

test('legacy Fire Browser same-origin sends have a stable request ID',()=>{
  const m=normalizeMessage({text:'TV test',id:'9b79725a-8097-432f-8dcc-c0986bf8da98'});
  assert.equal(m.id,'9b79725a-8097-432f-8dcc-c0986bf8da98');
  assert.equal(m.to,'human:owner');
  assert.equal(m.message,'TV test');
  assert.equal(publicMessage(m).message,'TV test');
});
test('LC1 payload remains byte-identical for existing Python agent adapter',()=>{
  const metadata={
    id:'ab9f83cc-0302-4bac-9b14-b948b2937230',from:'agent:alpha',to:'agent:beta',
    kind:'question',project:'fire/snake',reply_to:null,
    created_at:'2026-11-08T09:00:00Z',refs:[]
  };
  const wrapped='[LC1 '+JSON.stringify(metadata)+']\nCan you make Snake smoother?';
  assert.equal(parseWire(wrapped).to,'agent:beta');
  const m=normalizeMessage({text:wrapped,id:metadata.id});
  assert.equal(m.message,wrapped);
  assert.equal(m.text,'Can you make Snake smoother?');
  assert.equal(m.to,'agent:beta');
  assert.equal(m.created_at,metadata.created_at);
});
test('LC1 mismatched request ID is rejected instead of misrouting',()=>{
  const raw='[LC1 '+JSON.stringify({
    id:'abcdefgh',from:'agent:a',to:'agent:b',kind:'question'
  })+']\nHello';
  assert.throws(()=>normalizeMessage({text:raw,id:'ijklmnop'}),InputError);
});
test('invalid recipients, oversized messages, refs and unknown kinds fail',()=>{
  assert.throws(()=>normalizeMessage({text:'hello',to:'shell:root'}),InputError);
  assert.throws(()=>normalizeMessage({text:'x'.repeat(1601)}),InputError);
  assert.throws(()=>normalizeMessage({text:'hello',kind:'execute'}),InputError);
  assert.throws(()=>normalizeMessage({text:'hello',refs:['https://attacker.invalid/run']}),InputError);
});
test('historical message migration preserves original ID timestamp and full body',()=>{
  const text='A'.repeat(5000);
  const m=normalizeMessage({
    id:'historical-item-20261103',
    text, created_at:'2026-11-03T17:21:04.756Z'
  });
  assert.equal(m.id,'historical-item-20261103');
  assert.equal(m.message,text);
  assert.equal(m.created_at,'2026-11-03T17:21:04.756Z');
  assert.throws(()=>normalizeMessage({text,created_at:'not-a-date'}),InputError);
});
test('status parser accepts exactly the legacy values',()=>{
  assert.equal(parseDone('1'),true);
  assert.equal(parseDone('0'),false);
  assert.throws(()=>parseDone('maybe'),InputError);
});
test('untrusted messages remain data, never commands',()=>{
  const m=normalizeMessage({text:'rm -rf /',kind:'request'});
  assert.equal(m.message,'rm -rf /');
  assert.equal(m.to,'human:owner');
});
