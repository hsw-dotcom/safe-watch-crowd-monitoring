"""Validate structural dependencies without starting any server."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'src/web'
expected={
    'index.html','graph.html','map.html','image.html','api.php',
    'assets/dashboard.js','assets/chart.js','assets/style.css','assets/demo-data.json',
}
assert all((WEB / name).is_file() for name in expected), 'Missing required web file'
assert len(list(WEB.glob('*.php'))) == 1, 'Only one PHP API should remain'
for html in WEB.glob('*.html'):
    content=html.read_text(encoding='utf-8')
    for ref in re.findall(r'(?:src|href|data-src)="([^"]+)"', content):
        if ref.startswith(('http:','https:','#','data:','/tensorflow/')) or ref=='warning.wav': continue
        assert (WEB/ref).exists(), f'{html.name}: missing {ref}'
for p in ['main.py','stream.py','alarm.py','count_objects.py','db.py','settings.py','risk.py','configs.ini']:
    assert (ROOT/'src/python'/p).is_file(), p
assert not (ROOT/'src/python/app.py').exists()
assert (ROOT/'database/schema.sql').is_file()
print('Structure/reference verification passed.')
