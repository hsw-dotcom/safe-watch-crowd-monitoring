# 2023년 프로젝트 대화에서 확인되는 HTML 이미지 갱신 예시

질문과 답변에서 `setInterval(updateImage, 2000)`와 새 타임스탬프를 활용한 캐시 무효화(`?` + `new Date().getTime()`)를 반복적으로 사용했습니다.
브라우저에서 라즈베리파이의 실제 파일 시스템 절대경로(`/home/pi/project/output/after.jpg`)를 직접 읽게 하면 웹 서버에 그 경로가 노출되지 않아 실패할 수 있습니다.

당시 최종 코드와 연결되는 경로는 `/var/www/html/tensorflow/after.jpg`이며, HTML URL은 `/tensorflow/after.jpg`가 됩니다.

```javascript
setInterval(updateImage, 2000);
function updateImage() {
  var imgElement = document.getElementById('afterImage');
  imgElement.src = '/tensorflow/after.jpg?' + new Date().getTime();
}
```

이 문서는 완전한 2023 채팅 로그가 아니라, 확인 가능한 문답 조각에 따른 복원 근거 설명입니다.
