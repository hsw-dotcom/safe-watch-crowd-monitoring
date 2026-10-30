"""Check static references without needing MariaDB/Camera."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
web=ROOT/'02_nginx_webroot'
expected=[
  'index.html','maininfo.html','graph.html','map.html','density.html','change.html',
  'image.php','maininfo.php','densityinfo.php','changeinfo.php','db_connect.php',
  'assets/dashboard.js','assets/chart.js','assets/style.css',
]
for name in expected:
    assert (web/name).is_file(), name
for html in web.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    for ref in re.findall(r'(?:src|href)="([^"]+)"', text):
        if ref.startswith(('http:','https:','#','data:')) or ref in ('warning.wav',):continue  # external or known missing original asset
        assert (web/ref).exists(), f'{html.name} references nonexistent {ref}'
for name in ['main.py','stream.py','alarm.py','count_objects.py','db.py','settings.py','risk.py','app.py']:
    assert (ROOT/'01_raspberry_pi_project'/name).exists(),name
assert (ROOT/'03_database'/'schema.sql').is_file()
print('Structure/reference test passed')
