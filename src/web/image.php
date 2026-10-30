<!DOCTYPE html>
<html>
<head>
  <script>
    setInterval(updateImage, 2000);

    function updateImage() {
      // 이미지 업데이트 로직
      var imgElement = document.getElementById('afterImage');
      imgElement.src = "/tensorflow/after.jpg?" + new Date().getTime();
    }
  </script>
  <style>
    img {
      width: 800px;
      height: 470px;
    }
  </style>
</head>
<body>
  <img id="afterImage" src="/tensorflow/after.jpg" alt="After Image">
</body>
</html>
