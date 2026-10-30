"""2023 model-inference path reconstructed from original count_objects.py.

The model is loaded as a fixed TFLite file; this module does NOT train,
convert, or alter model weights after export. Only image detection is used.
The original disabled obstacle detection, which remains disabled here.
"""
import os
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = HERE / 'models' / 'people_detect.tflite'
LABEL = HERE / 'models' / 'people_label.txt'
INPUT_IMAGE = HERE / 'image' / 'before.jpg'
OUTPUT_IMAGE = Path(os.getenv('SAFEWATCH_AFTER_IMAGE', '/var/www/html/tensorflow/after.jpg'))
MIN_CONFIDENCE = 0.2  # original threshold
PERSON_CLASS_ID = 0   # original class


def load_model():
    """Load the already-exported model without modification, like 2023 code."""
    if not MODEL.is_file() or not LABEL.is_file():
        raise FileNotFoundError('2023 TFLite model/label assets are not available')
    try:
        from tflite_runtime.interpreter import Interpreter
    except ImportError:
        from tensorflow.lite.python.interpreter import Interpreter
    interpreter = Interpreter(model_path=str(MODEL))
    interpreter.allocate_tensors()
    labels = LABEL.read_text(encoding='utf-8-sig').splitlines()
    return interpreter, labels


def get_outputs(interpreter):
    details = interpreter.get_output_details()
    if len(details) < 3:
        raise RuntimeError('지원하지 않는 모델 출력 구조입니다.')
    out_name = details[0]['name']
    if 'StatefulPartitionedCall' in out_name:
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:
        boxes_idx, classes_idx, scores_idx = 0, 1, 2
    if max(boxes_idx, classes_idx, scores_idx) >= len(details):
        raise RuntimeError('모델 출력 텐서를 확인해야 합니다.')
    boxes = np.asarray(interpreter.get_tensor(details[boxes_idx]['index']))[0]
    classes = np.asarray(interpreter.get_tensor(details[classes_idx]['index']))[0]
    scores = np.asarray(interpreter.get_tensor(details[scores_idx]['index']))[0]
    return boxes, classes, scores


def detect(image_path=None, output_path=None):
    """Return (people_count, disabled_obstacle_classes) as original did."""
    import cv2
    src = Path(image_path) if image_path else INPUT_IMAGE
    dst = Path(output_path) if output_path else OUTPUT_IMAGE
    image = cv2.imread(str(src))
    if image is None:
        raise FileNotFoundError(f'인식할 이미지를 찾을 수 없습니다: {src}')
    interpreter, labels = load_model()
    input_details = interpreter.get_input_details()[0]
    ih, iw = (int(v) for v in input_details['shape'][1:3])
    resized = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), (iw, ih))
    data = np.expand_dims(resized, axis=0)
    if input_details['dtype'] == np.float32:
        data = (data.astype(np.float32) - 127.5) / 127.5
    interpreter.set_tensor(input_details['index'], data)
    interpreter.invoke()
    boxes, classes, scores = get_outputs(interpreter)
    h, w = image.shape[:2]
    people_count = 0
    for bbox, cls, score in zip(boxes, classes, scores):
        if float(score) < MIN_CONFIDENCE or int(cls) != PERSON_CLASS_ID:
            continue
        people_count += 1
        ymin, xmin, ymax, xmax = (float(v) for v in bbox)
        x1 = max(0, min(w - 1, int(xmin * w)))
        x2 = max(0, min(w - 1, int(xmax * w)))
        y1 = max(0, min(h - 1, int(ymin * h)))
        y2 = max(0, min(h - 1, int(ymax * h)))
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        if 0 <= int(cls) < len(labels):
            caption = f'{labels[int(cls)]}: {float(score):.0%}'
            cv2.putText(image, caption, (x1, max(20, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    dst.parent.mkdir(parents=True, exist_ok=True)
    # 2023 source overwrote after.jpg directly, not via an atomic tmp file.
    if not cv2.imwrite(str(dst), image):
        raise OSError(f'검출 이미지 저장에 실패했습니다: {dst}')
    return people_count, []
