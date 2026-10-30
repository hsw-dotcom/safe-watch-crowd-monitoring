"""Reconstructed application settings; historical defaults are preserved where possible."""
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
    safe_max: float
    danger_min: float
    min_confidence: float
    person_class_id: int

def load_config(path=None):
    cfg = configparser.ConfigParser()
    target = Path(path) if path else HERE / 'configs.ini'
    if not cfg.read(target, encoding='utf-8'):
        raise FileNotFoundError(f'설정 파일이 없습니다: {target}')
    section = cfg['settings']
    s = Settings(
        delay=section.getfloat('delay', fallback=15),
        total_area=section.getfloat('total_area', fallback=300),
        camera_number=section.getint('camera_number', fallback=1),
        max_iterations=section.getint('max_iterations', fallback=0),
        stream_url=os.getenv('SAFEWATCH_STREAM_URL', section.get('stream_url', fallback='http://127.0.0.1:8000/stream.mjpg')),
        safe_max=section.getfloat('safe_max', fallback=2),
        danger_min=section.getfloat('danger_min', fallback=4),
        min_confidence=section.getfloat('min_confidence', fallback=0.2),
        person_class_id=section.getint('person_class_id', fallback=0),
    )
    if s.delay <= 0 or s.total_area <= 0 or s.camera_number < 1 or s.safe_max >= s.danger_min:
        raise ValueError('delay/total_area/camera_number/위험 기준값 설정이 잘못되었습니다.')
    return s
