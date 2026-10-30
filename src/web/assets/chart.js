"use strict";
// One history request feeds both charts; no separate density/change pages or PHP endpoints.
const demo = new URLSearchParams(location.search).get('demo') === '1';
const errorBox = document.getElementById('chart-error');
if (demo) {
  document.getElementById('demo-label').hidden = false;
  document.getElementById('home-link').href = 'index.html?demo=1';
}
let densityChart, changeChart;

async function historyRows() {
  const response = await fetch(demo ? 'assets/demo-data.json' : 'api.php?view=history', {cache: 'no-store'});
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const json = await response.json();
  const rows = demo ? json.history : json;
  if (!Array.isArray(rows)) throw new Error('API history 형식이 올바르지 않습니다.');
  return rows;
}

function createChart(elementId, label, beginAtZero) {
  return new Chart(document.getElementById(elementId), {
    type: 'line',
    data: {labels: [], datasets: [{label, data: [], borderColor: '#2563eb',
      backgroundColor: 'rgba(37,99,235,.12)', fill: true, tension: .2, spanGaps: false}]},
    options: {responsive: true, maintainAspectRatio: false, animation: false,
      scales: {y: {beginAtZero}}}
  });
}

async function refreshCharts() {
  try {
    const rows = await historyRows();
    const labels = rows.map(row => row.time_label);
    densityChart.data.labels = labels;
    densityChart.data.datasets[0].data = rows.map(row => row.crowd_density);
    changeChart.data.labels = labels;
    changeChart.data.datasets[0].data = rows.map(row => row.change_rate);
    densityChart.update();
    changeChart.update();
    errorBox.textContent = '';
  } catch (e) {
    errorBox.textContent = '그래프 데이터 조회 오류: ' + e.message;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (typeof Chart === 'undefined') {
    errorBox.textContent = 'Chart.js 로딩 실패: 네트워크 연결이 필요합니다.';
    return;
  }
  densityChart = createChart('density-chart', '군중 밀집도', true);
  changeChart = createChart('change-chart', '밀집도 변화율 (%)', false);
  refreshCharts();
  if (!demo) setInterval(refreshCharts, 5000);
});
