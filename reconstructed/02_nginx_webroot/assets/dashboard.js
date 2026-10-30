'use strict';
let currentAlertId = null;
let audioEnabled = false;
let lastLevel = null;
const $ = id => document.getElementById(id);
const fmt = n => n == null ? '—' : String(n);
const elapsed = () => new Date().toLocaleTimeString('ko-KR', {hour12:false});

function configureAudio(){
  const button = $('enable-audio');
  if (!button) return;
  button.addEventListener('click',()=>{
    audioEnabled = true;
    button.textContent='경고음 사용 설정됨';
    button.disabled=true;
  });
}
function playDangerSound(){
  if (!audioEnabled) return; // browser autoplay policy requires explicit user gesture.
  const audio = $('alarm-audio');
  if (audio) audio.play().catch(()=>{});
}
async function refreshStatus(){
  try{
    const res=await fetch('maininfo.php',{cache:'no-store'});
    if(!res.ok) throw new Error(`서버 응답 ${res.status}`);
    const data=await res.json();
    if(!Array.isArray(data)||data.length===0){
      $('error').textContent='측정 데이터가 없습니다.';return;
    }
    const item=data[0], level=item.danger_level;
    $('people').textContent=fmt(item.people_count);
    $('density').textContent=Number(item.crowd_density).toFixed(4);
    $('level').textContent=fmt(level);
    $('measured').textContent=fmt(item.update_time);
    $('status').className='status '+(level==='위험'?'danger':level==='경고'?'warning':'safe');
    $('error').textContent='';
    // Historical UI modal/audio preserved without undocumented browser-side SMS.
    const isNewDanger=level==='위험' && lastLevel!=='위험' && item.id!==currentAlertId;
    if(isNewDanger){
      $('danger-notice').classList.remove('hidden');
      playDangerSound();
      currentAlertId=item.id;
    }else if(level!=='위험'){
      $('danger-notice').classList.add('hidden');
    }
    lastLevel=level;
  }catch(err){$('error').textContent='데이터 연결 오류: '+err.message;}
}
document.addEventListener('DOMContentLoaded',()=>{
  configureAudio();
  $('time').textContent=elapsed();
  setInterval(()=>$('time').textContent=elapsed(),1000);
  refreshStatus();setInterval(refreshStatus,5000);
});
