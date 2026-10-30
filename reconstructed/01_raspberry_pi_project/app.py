"""OPTIONAL reconstructed local Flask endpoint from 2023 '/send_sms' discussion.

The 2023 original Flask app.py was NOT recovered. Not used by index.html and
not necessary for the normal alarm.py flow. Localhost-bound + POST + token.
"""
import os
import time
from flask import Flask, jsonify, request
from alarm import send_sms

app = Flask(__name__)
_last_call = 0.0

@app.post('/send_sms')
def send_sms_route():
    global _last_call
    token = os.getenv('SAFEWATCH_MANUAL_API_TOKEN')
    provided = request.headers.get('X-SafeWatch-Token', '')
    if not token or not provided:
        return jsonify(error='Manual SMS route disabled or unauthenticated'), 403
    import hmac
    if not hmac.compare_digest(provided, token):
        return jsonify(error='Invalid token'), 403
    if time.monotonic() - _last_call < 300:
        return jsonify(error='Cooldown active'), 429
    _last_call = time.monotonic()
    try:
        if send_sms():
            return jsonify(status='Twilio accepted message request'), 200
        return jsonify(error='SMS not enabled or credentials unavailable'), 503
    except Exception:
        app.logger.exception('Twilio API error')
        return jsonify(error='SMS API request failed'), 502

if __name__ == '__main__':
    # Do NOT bind to 0.0.0.0 or publish through ipTIME DMZ.
    app.run(host='127.0.0.1', port=5000, debug=False)
