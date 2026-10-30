"""2023 Safe Watch capture → fixed-model detection → density/stage → DB.

2023 project used a fixed total_area and overwrote before.jpg for each sample.
This reconstruction preserves that behavior. --dry-run is a new offline test aid.
"""
import argparse
import logging
import time
from pathlib import Path

from settings import load_config
from risk import evaluate

HERE = Path(__file__).resolve().parent
LOG = logging.getLogger('safewatch')


def capture_frame(stream_url, image_path):
    import cv2
    capture = cv2.VideoCapture(stream_url)
    try:
        if not capture.isOpened():
            raise OSError(f'MJPEG 연결에 실패했습니다: {stream_url}')
        ok, frame = capture.read()
        if not ok or frame is None:
            raise OSError('스트림에서 프레임을 가져오지 못했습니다.')
        image_path.parent.mkdir(parents=True, exist_ok=True)
        # Historical behavior: the SAME before.jpg is overwritten on each sample.
        if not cv2.imwrite(str(image_path), frame):
            raise OSError(f'이미지 저장 실패: {image_path}')
    finally:
        capture.release()


def run(config_file=None, dry_run=False, samples=(0, 1, 2, 3, 4, 5, 6), iterations=None):
    from count_objects import detect
    from db import save_measurement
    cfg = load_config(config_file)
    limit = cfg.max_iterations if iterations is None else iterations
    index = 0
    while limit == 0 or index < limit:
        started = time.monotonic()
        try:
            if dry_run:
                people_count = samples[index % len(samples)]
            else:
                capture_frame(cfg.stream_url, HERE / 'image' / 'before.jpg')
                people_count, _obstacles = detect()
            # Do not dynamically calculate the area or use obstacle area.
            crowd_density, level = evaluate(people_count, cfg.total_area)
            saved_id = 'DRY-RUN (미저장)' if dry_run else save_measurement(crowd_density, level)
            LOG.info('인식 인원=%d 고정면적=%.1f 밀집도=%.4f 상태=%s DB=%s',
                     people_count, cfg.total_area, crowd_density, level, saved_id)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            LOG.exception('처리 중 오류; 다음 회차에서 재시도합니다.')
        index += 1
        # Historical script computed elapsed time but actually slept the full delay.
        if not dry_run:
            time.sleep(cfg.delay)


def main():
    parser = argparse.ArgumentParser(description='Safe Watch 2023 code reconstruction')
    parser.add_argument('--config', default=None)
    parser.add_argument('--dry-run', action='store_true', help='카메라/모델/DB 없는 합성 입력 테스트 전용')
    parser.add_argument('--iterations', type=int, default=None, help='0이면 무한 반복')
    args = parser.parse_args()
    if args.iterations is not None and args.iterations < 0:
        parser.error('--iterations는 0 이상이어야 합니다.')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    limit = (5 if args.dry_run else None) if args.iterations is None else args.iterations
    try:
        run(config_file=args.config, dry_run=args.dry_run, iterations=limit)
    except KeyboardInterrupt:
        LOG.info('종료')

if __name__ == '__main__':
    main()
