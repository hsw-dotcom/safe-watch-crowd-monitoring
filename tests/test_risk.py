"""Executable CPU-only tests; do not imply Pi camera/model/SMS has been tested."""
from pathlib import Path
import sys
import unittest

SRC = Path(__file__).resolve().parents[1] / 'src' / 'python'
sys.path.insert(0, str(SRC))
from risk import calculate_density, danger_level, evaluate
from settings import load_config
from alarm import should_alert

class RiskTest(unittest.TestCase):
    def test_calculate(self):
        self.assertEqual(calculate_density(10, 5), 2.0)
        self.assertEqual(calculate_density(0, 100), 0.0)

    def test_boundaries(self):
        self.assertEqual(danger_level(2), '안전')
        self.assertEqual(danger_level(2.01), '경고')
        self.assertEqual(danger_level(3.99), '경고')
        self.assertEqual(danger_level(4), '위험')

    def test_input_validation(self):
        with self.assertRaises(ValueError): calculate_density(1, 0)
        with self.assertRaises(ValueError): calculate_density(-1, 5)
        with self.assertRaises(ValueError): danger_level(2, 4, 2)

    def test_config_historical_defaults(self):
        cfg = load_config()
        self.assertEqual(cfg.delay, 15)
        self.assertEqual(cfg.total_area, 300)
        self.assertEqual(cfg.stream_url.endswith('/stream.mjpg'), True)

    def test_alarm_transition_and_cooldown(self):
        danger = {'id': 101, 'danger_level':'위험'}
        self.assertTrue(should_alert(100, '안전', danger, 0, 400, 300))
        self.assertFalse(should_alert(101, '위험', danger, 0, 400, 300))
        self.assertFalse(should_alert(100, '안전', danger, 400, 401, 300))
        self.assertFalse(should_alert(100, '안전', {'id': 101, 'danger_level':'경고'}, 0, 400, 300))

if __name__ == '__main__': unittest.main()
