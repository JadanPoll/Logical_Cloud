/* Identity is an address-book convenience, not authentication.
 * Browser-local record survives ordinary reloads and deployments.
 * Fire Browser provides its own persistent native sender ID in ?from=.
 */
(function (root) {
  'use strict';
  const KEY='fire_inbox_identity_v1';
  const ADDRESS=/^device:[a-z0-9][a-z0-9._/-]{0,63}$/;
  const FIRE=/^device:fire-tv-[a-f0-9]{12}$/;
  function randomAddress() {
    let suffix='';
    try {
      const arr=new Uint8Array(6);
      root.crypto.getRandomValues(arr);
      suffix=Array.from(arr, x=>x.toString(16).padStart(2,'0')).join('');
    } catch {
      // Random IDs are for correlation, never for security. An unseeded
      // browser without working crypto/storage must not claim persistence.
      suffix='temporary';
    }
    return 'device:browser-'+suffix;
  }
  function safeStorage(storage,mode,value) {
    try {
      if(mode==='get') return JSON.parse(storage.getItem(KEY)||'null');
      storage.setItem(KEY,JSON.stringify(value));
      return true;
    } catch { return mode==='get'?null:false; }
  }
  function cleanLabel(value) {
    return typeof value==='string'&&value.trim()&&!/[\r\n\u0000-\u001f]/.test(value)
      ? value.trim().slice(0,48) : null;
  }
  function load(storage,seed) {
    const saved=safeStorage(storage,'get');
    const previous=saved&&typeof saved==='object'&&ADDRESS.test(saved.id)?saved:null;
    // A Fire TV native ID is the authority for THIS local installation.
    // Arbitrary URL 'from' values do not overwrite a browser identity.
    const id=typeof seed==='string'&&FIRE.test(seed)?seed:
      previous?previous.id:randomAddress();
    const same=previous&&previous.id===id;
    const label=same?cleanLabel(previous.label):null;
    const item={
      id,label:label||(FIRE.test(id)?'Fire TV':'This browser'),
      persistent:false
    };
    item.persistent=safeStorage(storage,'set',{id:item.id,label:item.label});
    return item;
  }
  function rename(storage,current,next) {
    const label=cleanLabel(next);
    if(!label) throw new Error('Use a short recognizable device name');
    const updated={id:current.id,label,persistent:false};
    updated.persistent=safeStorage(storage,'set',{id:updated.id,label});
    return updated;
  }
  root.FireInboxIdentity={load,rename};
})(typeof window!=='undefined'?window:globalThis);
