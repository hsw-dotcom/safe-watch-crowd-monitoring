# Historical troubleshooting (2023)

## MJPEG camera streaming

The individual final report documents several failed attempts before the MJPEG stream displayed successfully in the website. The same camera stream was needed by frame-capture code feeding the object detector. Submitted source uses a Picamera2 MJPEG encoder and an HTTP server on port 8000. The report does not identify one reproducible root cause or exact sequence of fixes; do not claim a specific configuration tweak without evidence.

## USB speaker vs browser audio

The report describes that a physically connected speaker initially failed to play from Python, while browser audio could play on the viewing PC/mobile instead of the Raspberry Pi. The submitted `alarm.py` uses `subprocess.run(["aplay", "-D", "hw:3", ...])` to target an audio device. The report claims the intended arrangement was achieved after modifications. Separate field-triggered danger SMS+speaker playback was not validated because real testing did not reach the danger level.

## Testing limitations

- Raspberry Pi 4 and Camera Module 3 were used in 2023 but hardware is no longer available for retesting.
- Model files and Flask SMS server script are not archived.
- Fixed area value and limited recognition range constrained the accuracy of crowd density inference.
- The known results are historical prototype tests rather than deployment to a real public safety infrastructure.
