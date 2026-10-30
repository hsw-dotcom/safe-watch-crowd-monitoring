# Attribution and historical source provenance

**Team project (2023):** The capstone was performed by four students. The individual final report documents distinct roles across AI training, density calculation research, device assembly, and web/DB/streaming/alert work. This repo preserves a selection of archived group source. Avoid interpreting the repository account as sole author of all modules.

**TensorFlow Lite object detection:** The header of `src/python/count_objects.py` describes an object-detection example by Evan Juras and references a TensorFlow Lite example: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py . Related example project: https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi . The adapted file should not be described as independently designed object-detection architecture.

**Camera streaming:** `src/python/stream.py` retains an original comment noting that it follows an MJPEG server example using a hardware encoder. Refer to official Picamera2 examples and their associated licensing before redistributing substantial portions.

**Other dependencies:** Chart.js, jQuery, Moment.js, PHP, Nginx, MariaDB, OpenCV, TensorFlow Lite, Twilio, and Picamera2 are external components with their own licenses/terms. No proprietary model, dataset, Colab notebook (which contains third-party and credential concerns), or copyrighted images are distributed here.

**License status:** No blanket LICENSE file was added; ownership and reuse rights of legacy code were not independently verified.
