"""Self-contained offline dashboard: variant comparison and cross-device timeline."""
from __future__ import annotations
import json


def render_html(cases: list[dict]) -> str:
    # Escaped JSON prevents a scenario name from breaking out of the script tag.
    dataset = json.dumps(cases, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logical Cloud — Experiment Explorer</title>
<style>
:root{color-scheme:light;font-family:system-ui,-apple-system,Segoe UI,sans-serif}
body{max-width:1300px;margin:auto;padding:28px;background:#f8fafc;color:#172337}
h1{margin:0 0 4px;font-size:1.9rem}p{color:#465469;line-height:1.5}
section{background:white;border:1px solid #d8dfe7;border-radius:12px;padding:20px;margin:20px 0;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;border-bottom:1px solid #e7ebf0;padding:9px}
th{background:#f1f5f9}tr.pick{cursor:pointer}tr.pick:hover{background:#e7f1ff}tr.active{background:#dceafa}
select{padding:8px;border:1px solid #aebaca;border-radius:8px;min-width:260px;font-size:15px}
.metrics{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0}.metric{background:#f1f5f9;padding:12px;border-radius:9px;min-width:150px}
.metric strong{display:block;font-size:1.4rem}.metric small{color:#526174}
#timeline{display:block;width:100%;min-width:650px;border:1px solid #e1e6ee;background:white}
.legend{display:flex;flex-wrap:wrap;gap:18px;font-size:13px;color:#465469;margin:12px 0}
.swatch{display:inline-block;width:14px;height:14px;vertical-align:middle;margin-right:6px;border-radius:3px}
pre{max-height:420px;overflow:auto;background:#0f172a;color:#e2e8f0;padding:14px;border-radius:8px;font-size:12px}
</style></head>
<body><h1>Logical Cloud · Experiment Explorer</h1>
<p>Every run uses the same declarative application; variants substitute named placement and infrastructure factors. The discrete-event model estimates CPU queues, code caching and network transfers. These are simulated predictions, not measurements from real devices.</p>
<section><h2>Factorial comparison</h2><table id="variants"><thead><tr><th>Variant</th><th>p50 (ms)</th><th>p95 (ms)</th><th>Total link bytes</th><th>Code fetches</th><th>Result</th></tr></thead><tbody></tbody></table></section>
<section><h2>Split execution timeline</h2><label for="case">Experiment:</label> <select id="case"></select>
<div class="metrics" id="metrics"></div><div class="legend">
<span><i class="swatch" style="background:#2463a8"></i>CPU work</span>
<span><i class="swatch" style="background:#df9645"></i>Input/data/result transfer</span>
<span><i class="swatch" style="background:#9c58bb"></i>Code fetch</span></div>
<svg id="timeline" viewBox="0 0 1100 300" aria-label="Time along horizontal axis, rows for devices and transfers" role="img"></svg>
<details><summary>Machine-readable event trace</summary><pre id="trace"></pre></details></section>
<p>Model scope: deterministic, FIFO non-preemptive CPU slots, per-direction link serialization, store-and-forward routing, per-device LRU code caches. No live runtime or observed QoS measurements are implied.</p>
<script>
const cases = __CASE_DATA__;
const NS='http://www.w3.org/2000/svg';
const $=id=>document.getElementById(id);
function el(tag,attrs={},text){const node=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))node.setAttribute(k,String(v));if(text!==undefined)node.textContent=text;return node;}
function metric(label,value){let box=document.createElement('div');box.className='metric';let s=document.createElement('small');s.textContent=label;let b=document.createElement('strong');b.textContent=String(value);box.append(s,b);return box;}
function show(i){const c=cases[i];$('case').value=String(i);document.querySelectorAll('tr.pick').forEach((row,j)=>row.classList.toggle('active',i===j));
const m=$('metrics');m.replaceChildren(metric('p50 latency',c.p50_ms+' ms'),metric('p95 latency',c.p95_ms+' ms'),metric('Network hop bytes',c.network_bytes_total.toLocaleString()),metric('Code fetches',c.counters.artifact_fetches||0),metric('Cache hits',c.counters.cache_hits||0));
$('trace').textContent=JSON.stringify(c.trace,null,2);
const active=new Map(),bars=[];const deviceIds=Object.keys(c.cpu_busy_ms_by_device);deviceIds.forEach(x=>{});
for(const e of c.trace){if(e.event==='stage_started'){active.set(e.invocation+':'+e.stage,{at:e.at_ms,...e});}
if(e.event==='stage_completed'){const old=active.get(e.invocation+':'+e.stage);if(old){bars.push({lane:old.device,start:old.at,end:e.at_ms,kind:'cpu',title:`request ${e.invocation}, ${e.stage} on ${old.device}`});active.delete(e.invocation+':'+e.stage);}}}
const transfers=new Map();for(const e of c.trace){if(e.event==='transfer_requested')transfers.set(e.transfer,e);
else if(e.event==='transfer_arrived'){const old=transfers.get(e.transfer);if(old)bars.push({lane:'network',start:old.at_ms,end:e.at_ms,kind:old.kind==='code'?'code':'data',title:`${old.kind}: ${old.bytes} bytes ${old.source} → ${old.destination}`});}}
const lanes=[...deviceIds,'network'];const svg=$('timeline');const width=1100,pad=116,right=32,rowH=52,header=38;const height=header+lanes.length*rowH+30;
svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${width} ${height}`);
const maxT=Math.max(1,c.makespan_ms);const x=t=>pad+(width-pad-right)*t/maxT;
for(let n=0;n<=5;n++){const t=maxT*n/5;svg.append(el('line',{x1:x(t),x2:x(t),y1:header-12,y2:height-25,stroke:'#d9e1ec','stroke-dasharray':'3 4'}));svg.append(el('text',{x:x(t),y:17,fill:'#526174','font-size':12,'text-anchor':'middle'},t.toFixed(1)+' ms'));}
lanes.forEach((lane,j)=>{const y=header+j*rowH;svg.append(el('rect',{x:0,y,width,height:rowH,fill:j%2?'#f8fafc':'#fff'}));svg.append(el('text',{x:12,y:y+rowH/2,fill:'#203047','font-size':13},lane));});
const color={cpu:'#2463a8',data:'#df9645',code:'#9c58bb'};
bars.sort((a,b)=>a.start-b.start).forEach(b=>{const j=lanes.indexOf(b.lane),y=header+j*rowH+12;if(j<0)return;let r=el('rect',{x:x(b.start),y,width:Math.max(2,x(b.end)-x(b.start)),height:26,rx:4,fill:color[b.kind],opacity:0.86});r.append(el('title',{},`${b.title}\n${b.start.toFixed(2)}–${b.end.toFixed(2)} ms`));svg.append(r);});
}
const tbody=document.querySelector('#variants tbody');const selector=$('case');cases.forEach((c,i)=>{let tr=document.createElement('tr');tr.className='pick';for(const value of [c.name,c.p50_ms,c.p95_ms,c.network_bytes_total,c.counters.artifact_fetches||0,'view timeline']){let td=document.createElement('td');td.textContent=String(value);tr.append(td);}tr.onclick=()=>show(i);tbody.append(tr);let opt=document.createElement('option');opt.value=String(i);opt.textContent=c.name;selector.append(opt);});selector.onchange=()=>show(Number(selector.value));if(cases.length)show(0);
</script></body></html>'''
    return page.replace('__CASE_DATA__', dataset)
