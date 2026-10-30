"""Historical config values are loaded; the zone area is fixed, not measured."""
import configparser
import os
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent

@dataclass(frozen=True)
class Settings:
    delay: float
    total_area: float
    camera_number: int
    max_iterations: int
    stream_url: str


def load_config(path=None):
    config = configparser.ConfigParser()
    target = Path(path) if path else HERE / 'configs.ini'
    if not config.read(target, encoding='utf-8'):
        raise FileNotFoundError(f'설정 파일을 찾을 수 없습니다: {target}')
    section = config['settings']
    cfg = Settings(
        delay=section.getfloat('delay', fallback=15),
        total_area=section.getfloat('total_area', fallback=300),
        camera_number=section.getint('camera_number', fallback=1),
        max_iterations=section.getint('max_iterations', fallback=100),
        stream_url=os.getenv('SAFEWATCH_STREAM_URL', section.get('stream_url', fallback='http://127.0.0.1:8000/stream.mjpg')),
    )
    if cfg.delay <= 0 or cfg.total_area <= 0 or cfg.camera_number < 1 or cfg.max_iterations < 0:
        raise ValueError('시간/고정면적/카메라번호/반복횟수 설정이 잘못되었습니다.')
    return cfg
