"""Safe Watch frame → TFLite → risk → MariaDB pipeline (reconstructed)."""
import argparse
import logging
import os
import time
from pathlib import Path

from settings import load_config
from risk import evaluate

HERE = Path(__file__).resolve().parent
LOG = logging.getLogger('safewatch')

def capture_frame(stream_url, image_path):
    import cv2
    cap = cv2.VideoCapture(stream_url)
    try:
        if not cap.isOpened():
            raise OSError(f'MJPEG 스트림에 연결할 수 없습니다: {stream_url}')
        ok, frame = cap.read()
        if not ok or frame is None:
            raise OSError('MJPEG 스트림에서 프레임을 가져오지 못했습니다.')
        image_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = image_path.with_name('before.tmp.jpg')
        if not cv2.imwrite(str(tmp), frame):
            raise OSError(f'이미지 저장 실패: {tmp}')
        tmp.replace(image_path)
    finally:
        cap.release()

def run(config_file=None, dry_run=False, samples=(0, 1, 2, 4, 10), iterations=None):
    from count_objects import detect
    from db import save_measurement
    cfg = load_config(config_file)
    index = 0
    limit = cfg.max_iterations if iterations is None else iterations
    while limit == 0 or index < limit:
        started = time.monotonic()
        try:
            if dry_run:
                # Demonstration only: no camera/model/DB/SMS interactions.
                people_count = samples[index % len(samples)]
            else:
                capture_frame(cfg.stream_url, HERE / 'image' / 'before.jpg')
                people_count, _unused_obstacles = detect(
                    confidence=cfg.min_confidence,
                    person_class_id=cfg.person_class_id)
            density, level = evaluate(people_count, cfg.total_area, cfg.safe_max, cfg.danger_min)
            if not dry_run:
                saved_id = save_measurement(cfg.camera_number, people_count, density, level)
            else:
                saved_id = 'DEMO (미저장)'
            LOG.info('카메라=%d 사람=%d 밀집도=%.4f 상태=%s ID=%s',
                     cfg.camera_number, people_count, density, level, saved_id)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            LOG.exception('한 번의 처리에서 오류 발생; 다음 반복에서 재시도합니다.')
        index += 1
        remaining = 0.0 if dry_run else max(0.0, cfg.delay - (time.monotonic() - started))
        try:
            time.sleep(remaining)
        except KeyboardInterrupt:
            break

def main():
    parser = argparse.ArgumentParser(description='Safe Watch 2023 reconstruction')
    parser.add_argument('--config', default=None)
    parser.add_argument('--dry-run', action='store_true', help='카메라/모델/DB 없이 합성 인원으로 계산 시연')
    parser.add_argument('--iterations', type=int, default=None, help='실행 횟수, 0이면 무한 반복')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    try:
        if args.iterations is not None and args.iterations < 0:
            parser.error("--iterations는 0 이상이어야 합니다.")
        iterations = 5 if args.dry_run and args.iterations is None else args.iterations
        run(config_file=args.config, dry_run=args.dry_run, iterations=iterations)
    except KeyboardInterrupt:
        LOG.info('종료')

if __name__ == '__main__':
    main()
