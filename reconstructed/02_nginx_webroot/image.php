<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;background:#0b1220}img{width:100%;height:100vh;object-fit:contain}</style></head>
<body><img id="afterImage" src="/tensorflow/after.jpg" alt="인원 검출 결과 (추론 후 표시)">
<script>
(function(){
  const img=document.querySelector('#afterImage');
  function refresh(){img.src='/tensorflow/after.jpg?t='+Date.now()}
  setInterval(refresh,2000); // Historical Q&A: timestamp avoids browser image caching.
})();
</script></body></html>
