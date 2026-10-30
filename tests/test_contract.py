"""Code-only checks: no hardware, database, model, PHP server or network required."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'src'/'web'

class ContractTest(unittest.TestCase):
    def test_demo_fixture_and_legacy_risk(self):
        data=json.loads((WEB/'assets/demo-data.json').read_text(encoding='utf-8'))
        self.assertEqual(data['latest']['danger_level'], '경고')
        self.assertAlmostEqual(data['latest']['people_count']/300, data['latest']['crowd_density'])
        self.assertEqual(len(data['history']), 7)

    def test_one_php_api(self):
        self.assertEqual([p.name for p in WEB.glob('*.php')], ['api.php'])
        body=(WEB/'api.php').read_text(encoding='utf-8')
        self.assertIn("['latest', 'history']", body)
        self.assertIn('WHERE camera_number = ?', body)

    def test_one_dashboard_and_one_chart_page(self):
        files={p.name for p in WEB.glob('*.html')}
        self.assertIn('index.html', files)
        self.assertIn('graph.html', files)
        for duplicate in ('density.html','change.html','maininfo.html','image.php'):
            self.assertNotIn(duplicate, files)

    def test_api_references(self):
        dashboard=(WEB/'assets/dashboard.js').read_text(encoding='utf-8')
        chart=(WEB/'assets/chart.js').read_text(encoding='utf-8')
        self.assertIn('api.php?view=latest', dashboard)
        self.assertIn('api.php?view=history', chart)
        self.assertIn('assets/demo-data.json', dashboard)
        self.assertIn('assets/demo-data.json', chart)

if __name__=='__main__': unittest.main()
