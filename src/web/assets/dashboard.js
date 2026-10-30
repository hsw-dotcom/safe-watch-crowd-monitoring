"use strict";
// One dashboard view, one JSON API. Demo mode uses synthetic local JSON (no Pi/DB/PHP).
const demo = new URLSearchParams(location.search).get('demo') === '1';
const $ = id => document.getElementById(id);
const fmt = v => v == null ? '—' : String(v);
let lastLevel = null;
let audioEnabled = false;

function setupFrames() {
  const live = $('live-camera');
  const detected = $('detected-camera');
  if (demo) {
    $('demo-label').hidden = false;
    $('graphs-link').href = 'graph.html?demo=1';
    const placeholder = label => `<html lang="ko"><body style="background:#0b1220;color:#cbd5e1;display:grid;place-items:center;height:90vh;font:16px sans-serif;text-align:center"><p>${label}<br>하드웨어가 없는 코드 확인용 화면</p></body></html>`;
    live.srcdoc = placeholder('실시간 카메라 미연결');
    detected.srcdoc = placeholder('탐지 결과 이미지 미연결');
  } else {
    live.src = live.dataset.src;
    detected.src = detected.dataset.src;
  }
}

function setupAudio() {
  const button = $('enable-audio');
  button.addEventListener('click', () => {
    audioEnabled = true;
    button.textContent = '경고음 사용 설정됨';
    button.disabled = true;
  });
}

async function getLatest() {
  const response = await fetch(demo ? 'assets/demo-data.json' : 'api.php?view=latest', {cache: 'no-store'});
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  return demo ? data.latest : data;
}

async function refresh() {
  try {
    const row = await getLatest();
    if (!row) { $('error').textContent = '측정 데이터가 없습니다.'; return; }
    const level = row.danger_level;
    $('people').textContent = fmt(row.people_count);
    $('density').textContent = Number(row.crowd_density).toFixed(4);
    $('level').textContent = fmt(level);
    $('measured').textContent = fmt(row.update_time);
    $('status').className = 'status ' + (level === '위험' ? 'danger' : level === '경고' ? 'warning' : 'safe');
    $('error').textContent = '';
    if (level === '위험' && lastLevel !== '위험') {
      $('danger-notice').classList.remove('hidden');
      if (!demo && audioEnabled) $('alarm-audio').play().catch(() => {});
    } else if (level !== '위험') {
      $('danger-notice').classList.add('hidden');
    }
    lastLevel = level;
  } catch (e) { $('error').textContent = '데이터 연결 오류: ' + e.message; }
}

document.addEventListener('DOMContentLoaded', () => {
  setupFrames();
  setupAudio();
  const updateClock = () => { $('time').textContent = new Date().toLocaleTimeString('ko-KR', {hour12: false}); };
  updateClock();
  setInterval(updateClock, 1000);
  refresh();
  if (!demo) setInterval(refresh, 5000);
});
