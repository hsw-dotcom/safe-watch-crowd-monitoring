'use strict';
const chartType=document.body.dataset.chart;
const isChange=chartType==='change';
const title=isChange?'밀집도 변화율 (%)':'밀집도';
const field=isChange?'change_rate':'crowd_density';
const url=isChange?'changeinfo.php':'densityinfo.php';
let chart;
async function refresh(){
  try{
    const r=await fetch(url,{cache:'no-store'});
    if(!r.ok)throw new Error('HTTP '+r.status);
    const d=await r.json();
    if(!Array.isArray(d))throw new Error('Invalid JSON');
    document.getElementById('chart-error').textContent='';
    chart.data.labels=d.map(v=>v.time_label);
    chart.data.datasets[0].data=d.map(v=>v[field]);
    chart.update();
  }catch(e){document.getElementById('chart-error').textContent='차트 데이터 오류: '+e.message;}
}
document.addEventListener('DOMContentLoaded',()=>{
  if(typeof Chart==='undefined'){
    document.getElementById('chart-error').textContent='Chart.js 로딩 실패. 네트워크 연결을 확인하세요.';
    return;
  }
  chart=new Chart(document.getElementById('chart'),{
    type:'line',data:{labels:[],datasets:[{label:title,data:[],borderColor:'#2563eb',backgroundColor:'rgba(37,99,235,.12)',fill:true,tension:.2,spanGaps:false}]},
    options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:true}},scales:{y:{beginAtZero:!isChange}}}
  });
  refresh();setInterval(refresh,5000);
});
