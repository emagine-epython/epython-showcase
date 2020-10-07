#/bin/sh

chromium-browser --headless --disable-gpu --no-sandbox --remote-debugging-port=9222 &
python -m test
