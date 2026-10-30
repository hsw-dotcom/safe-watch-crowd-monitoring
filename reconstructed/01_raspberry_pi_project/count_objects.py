"""TFLite 사람 검출 재구성본. 모델 학습 또는 정확도 검증 코드는 아님.

역사적 source의 class==0, confidence>=0.2, 640 입력, 웹 이미지 저장을 유지하되
출력 tensor 대응/이미지 실제 크기 기준 box 계산/Interpreter 재사용을 보완했습니다.
"""
from pathlib import Path
import os
import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = HERE / 'models' / 'people_detect.tflite'
LABEL = HERE / 'models' / 'people_label.txt'
INPUT_IMAGE = HERE / 'image' / 'before.jpg'
WEB_IMAGE = Path(os.getenv('SAFEWATCH_AFTER_IMAGE', '/var/www/html/tensorflow/after.jpg'))
_cached = None

def _load_interpreter():
    global _cached
    if _cached is not None:
        return _cached
    if not MODEL.is_file() or not LABEL.is_file():
        raise FileNotFoundError(f'실제 TFLite 모델/라벨 파일이 필요합니다: {MODEL}, {LABEL}')
    try:
        from tflite_runtime.interpreter import Interpreter
    except ImportError:
        from tensorflow.lite.python.interpreter import Interpreter
    interpreter = Interpreter(model_path=str(MODEL))
    interpreter.allocate_tensors()
    labels = [line.strip() for line in LABEL.read_text(encoding='utf-8-sig').splitlines()]
    _cached = (interpreter, labels)
    return _cached

def _output_arrays(interpreter):
    details = interpreter.get_output_details()
    names = [d['name'].lower() for d in details]
    # Historical models used TF1 or TF2 detection heads. Preserve explicit fallback.
    if any('statefulpartitionedcall' in n for n in names):
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:
        boxes_idx, classes_idx, scores_idx = 0, 1, 2
    if len(details) < 3 or max(boxes_idx, classes_idx, scores_idx) >= len(details):
        raise RuntimeError('지원하지 않는 TFLite 모델 출력 형식입니다.')
    arr = [interpreter.get_tensor(d['index']) for d in details]
    boxes = np.squeeze(arr[boxes_idx])
    classes = np.ravel(arr[classes_idx])
    scores = np.ravel(arr[scores_idx])
    if boxes.ndim == 1:
        boxes = boxes.reshape((-1, 4))
    if boxes.ndim != 2 or boxes.shape[1] != 4:
        raise RuntimeError('TFLite bounding box 출력 형식을 확인해야 합니다.')
    return boxes, classes, scores

def detect(image_path=None, output_path=None, confidence=0.2, person_class_id=0):
    """Return (number_of_people, obstacle_classes), retaining historical interface."""
    import cv2
    image_path = Path(image_path) if image_path else INPUT_IMAGE
    output_path = Path(output_path) if output_path else WEB_IMAGE
    frame = cv2.imread(str(image_path))
    if frame is None:
        raise FileNotFoundError(f'입력 이미지를 읽을 수 없습니다: {image_path}')
    interpreter, labels = _load_interpreter()
    in_details = interpreter.get_input_details()[0]
    shape = in_details['shape']
    in_height, in_width = int(shape[1]), int(shape[2])
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    data = cv2.resize(rgb, (in_width, in_height))[np.newaxis, :]
    if in_details['dtype'] == np.float32:
        data = (data.astype(np.float32) - 127.5) / 127.5
    else:
        data = data.astype(in_details['dtype'])
    interpreter.set_tensor(in_details['index'], data)
    interpreter.invoke()
    boxes, classes, scores = _output_arrays(interpreter)
    h, w = frame.shape[:2]
    count = 0
    for i, (box, class_id, score) in enumerate(zip(boxes, classes, scores)):
        if float(score) < confidence or int(class_id) != person_class_id:
            continue
        count += 1
        ymin, xmin, ymax, xmax = [float(v) for v in box]
        x1, x2 = max(0, min(w-1, round(xmin*w))), max(0, min(w-1, round(xmax*w)))
        y1, y2 = max(0, min(h-1, round(ymin*h))), max(0, min(h-1, round(ymax*h)))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        if 0 <= int(class_id) < len(labels):
            label = f'{labels[int(class_id)]}: {float(score):.0%}'
            cv2.putText(frame, label, (x1, max(20, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_path.with_name(output_path.stem + '.tmp.jpg')
    if not cv2.imwrite(str(tmp), frame):
        raise OSError(f'탐지 이미지 저장 실패: {tmp}')
    tmp.replace(output_path)
    return count, []   # 장애물 탐지는 역사적 원본에서도 비활성화
