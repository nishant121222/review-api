from waitress import serve
from backend.wsgi import application
import sys
import logging

# Enable Waitress logging
logging.basicConfig(level=logging.INFO)

port = 8080  # default
if len(sys.argv) > 1:
    port = int(sys.argv[1])

print(f"Starting Waitress server on http://0.0.0.0:{port} ...")

serve(application, host='0.0.0.0', port=port)
