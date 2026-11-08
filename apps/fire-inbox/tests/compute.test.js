import test from 'node:test';
import assert from 'node:assert/strict';
import { summarize } from '../api/compute/inspect.js';

test('Compute report displays actual evidence not optimistic claims',()=>{
const report=summarize('JadanPoll/fire',{
  info:{description:'Fire TV development',default_branch:'main',
    pushed_at:'2026-11-08T10:00:00Z',updated_at:'2026-11-08T10:00:00Z',open_issues_count:7},
  commit:{sha:'f'.repeat(40),commit:{message:'Repair remote focus\nDetails',
    committer:{date:'2026-11-08T10:00:00Z'}},html_url:'https://github.com/JadanPoll/fire/commit/'+ 'f'.repeat(40)},
  prs:[{number:22,title:'Add capability',html_url:'https://github.com/JadanPoll/fire/pull/22',
    updated_at:'2026-11-08T11:00:00Z'}],
  runs:{workflow_runs:[{name:'Release APK',status:'completed',conclusion:'success',
    html_url:'https://github.com/JadanPoll/fire/actions/runs/42'}]}
});
assert.equal(report.repository,'JadanPoll/fire');
assert.equal(report.latest_commit.sha,'ffffffffffff');
assert.equal(report.latest_commit.title,'Repair remote focus');
assert.equal(report.open_prs.length,1);
assert.equal(report.workflow[0].conclusion,'success');
assert.match(report.note,/not physical-TV verification/);
});
test('report limits presentation to a few relevant items',()=>{
const report=summarize('JadanPoll/fire',{
info:{},commit:null,prs:Array.from({length:12},(_,i)=>({
  number:i+1,title:'P'.repeat(300),html_url:'https://github.com/JadanPoll/fire/pull/'+(i+1)
})),runs:{workflow_runs:[]}
});
assert.equal(report.open_prs.length,5);
assert.equal(report.open_prs[0].title.length,150);
});
