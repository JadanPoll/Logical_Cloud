import { InputError } from '../../lib/protocol.js';

const REPO = /^[a-zA-Z0-9_.-]{1,39}\/[a-zA-Z0-9_.-]{1,100}$/;
const GH = 'https://api.github.com';
const headers = {'Accept':'application/vnd.github+json','User-Agent':'fire-compute-v1'};
const urlFor = (repo,kind='') => GH+'/repos/'+repo+kind;

async function github(path) {
  const response = await fetch(path,{
    headers, signal:AbortSignal.timeout(7500),cache:'no-store'
  });
  if (response.status===404) throw new InputError('Public repository not found',404);
  if (response.status===403 || response.status===429)
    throw new InputError('GitHub request limit reached. Try again later.',503);
  if (!response.ok) throw new InputError('GitHub returned HTTP '+response.status,502);
  const body=await response.text();
  if(body.length>180000) throw new InputError('GitHub result exceeds safe limit',502);
  return JSON.parse(body);
}

function normalized(repo) {
  if(typeof repo!=='string'||!REPO.test(repo)||repo.includes('..'))
    throw new InputError('Use a public GitHub owner/repository, for example JadanPoll/fire');
  return repo;
}
function clean(value,max=140) {
  return String(value??'').replace(/[\u0000-\u001f]/g,' ').slice(0,max);
}

export function summarize(repo,source){
  const {info,commit,prs,runs}=source;
  return {
    repository:repo, link:'https://github.com/'+repo,
    description:clean(info.description,240),
    default_branch:clean(info.default_branch,100),
    pushed_at:info.pushed_at,
    updated_at:info.updated_at,
    open_issues_count:info.open_issues_count,
    latest_commit:commit?.sha?{
      sha:commit.sha.slice(0,12),
      title:clean(commit.commit?.message?.split('\n')[0],180),
      date:commit.commit?.committer?.date||null,
      url:commit.html_url
    }:null,
    open_prs:(prs||[]).slice(0,5).map(p=>({
      number:p.number,title:clean(p.title,150),url:p.html_url,
      updated_at:p.updated_at
    })),
    workflow:(runs?.workflow_runs||[]).slice(0,3).map(w=>({
      name:clean(w.name,100),status:w.status,conclusion:w.conclusion,
      url:w.html_url,updated_at:w.updated_at
    })),
    checked_at:new Date().toISOString(),
    note:'Public GitHub metadata; a successful workflow is not physical-TV verification.'
  };
}

export default async function handler(req,res) {
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='GET')return res.status(405).json({ok:false,error:'GET required'});
  try {
    const url=new URL(req.url,'https://localhost');
    const repo=normalized(url.searchParams.get('repo'));
    const info=await github(urlFor(repo));
    if(info.private)throw new InputError('Private repositories cannot be inspected anonymously',403);
    // A repository can have Actions disabled or one endpoint rate-limited.
    // The rest of a useful inspection must still succeed, with failures
    // prominently distinguished from a genuinely empty list.
    const [commitResult,prResult,runResult]=await Promise.allSettled([
      github(urlFor(repo,'/commits?per_page=1')),
      github(urlFor(repo,'/pulls?state=open&per_page=5')),
      github(urlFor(repo,'/actions/runs?per_page=3'))
    ]);
    const checks={
      latest_commit:commitResult.status==='fulfilled',
      pull_requests:prResult.status==='fulfilled',
      workflows:runResult.status==='fulfilled'
    };
    const summary=summarize(repo,{
      info,
      commit:checks.latest_commit?commitResult.value[0]:null,
      prs:checks.pull_requests?prResult.value:[],
      runs:checks.workflows?runResult.value:{workflow_runs:[]}
    });
    summary.checks=checks;
    return res.status(200).json({ok:true,summary});
  } catch(e) {
    const known=e instanceof InputError;
    console.error('Compute inspect',known?e.status:500,e?.message);
    return res.status(known?e.status:502).json({
      ok:false,error:known?e.message:'Could not inspect public GitHub work; no actions were performed'
    });
  }
}
