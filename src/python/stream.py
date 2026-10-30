"""Picamera2 → HTTP MJPEG 8000; reconstructed from the project source architecture."""
import io
import logging
import os
import socketserver
from http import server
from threading import Condition

PAGE = b'<html><body><img src="/stream.mjpg" width="802" height="474"></body></html>'

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = bytes(buf)
            self.condition.notify_all()
        return len(buf)

output = StreamingOutput()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(PAGE)))
            self.end_headers()
            self.wfile.write(PAGE)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', '0')
            self.send_header('Cache-Control', 'no-store, private')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    if frame is None:
                        continue
                    self.wfile.write(b'--FRAME\r\nContent-Type: image/jpeg\r\n')
                    self.wfile.write(('Content-Length: %d\r\n\r\n' % len(frame)).encode())
                    self.wfile.write(frame + b'\r\n')
            except (BrokenPipeError, ConnectionResetError):
                pass
        else:
            self.send_error(404)

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def main():
    from picamera2 import Picamera2
    from picamera2.encoders import MJPEGEncoder
    from picamera2.outputs import FileOutput
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={'size': (1920, 1080)}))
    picam2.start_recording(MJPEGEncoder(), FileOutput(output))
    try:
        bind = os.getenv('SAFEWATCH_STREAM_BIND', '0.0.0.0')
        port = int(os.getenv('SAFEWATCH_STREAM_PORT', '8000'))
        logging.info('MJPEG server: %s:%d', bind, port)
        with StreamingServer((bind, port), StreamingHandler) as httpd:
            httpd.serve_forever()
    finally:
        picam2.stop_recording()
        picam2.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
