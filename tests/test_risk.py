"""Offline verification of the 2023 final presentation's risk boundaries."""
from pathlib import Path
import sys
import unittest

SRC=Path(__file__).resolve().parents[1] / 'src' / 'python'
sys.path.insert(0,str(SRC))
from risk import calculate_density, danger_level, evaluate
from settings import load_config
from alarm import alert_if_danger


class PresentationRiskTest(unittest.TestCase):
    def test_final_slide_stages(self):
        for count, expected in ((0,'안전'),(1,'안전'),(2,'안전'),(3,'경고'),(4,'경고'),(5,'위험'),(6,'위험')):
            with self.subTest(count=count):
                self.assertEqual(danger_level(count),expected)

    def test_area_fixed_only_for_density(self):
        self.assertAlmostEqual(calculate_density(5,300),5/300)
        self.assertEqual(evaluate(5,300)[1],'위험')
        self.assertEqual(evaluate(3,300)[1],'경고')
        self.assertEqual(evaluate(2,300)[1],'안전')

    def test_negative_count_rejected(self):
        with self.assertRaises(ValueError): danger_level(-1)
        with self.assertRaises(ValueError): calculate_density(-1,300)
        with self.assertRaises(ValueError): calculate_density(1,0)

    def test_historical_fixed_defaults(self):
        cfg=load_config()
        self.assertEqual(cfg.delay,15)
        self.assertEqual(cfg.total_area,300)
        self.assertEqual(cfg.max_iterations,100)

    def test_original_repeated_alert_behavior(self):
        calls=[]
        def sound(): calls.append('sound')
        def sms(level): calls.append(level)
        self.assertFalse(alert_if_danger('경고',sound=sound,sms=sms))
        self.assertTrue(alert_if_danger('위험',sound=sound,sms=sms))
        self.assertTrue(alert_if_danger('위험',sound=sound,sms=sms))
        self.assertEqual(calls,['위험','sound','위험','sound'])

if __name__=='__main__':unittest.main()
