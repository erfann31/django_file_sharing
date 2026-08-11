import os
import socket
import threading
import time
import webbrowser
import sys

# Fake stdout/stderr for PyInstaller --noconsole
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")

if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


ip = get_local_ip()
port = 8000

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_manager.settings")
os.environ.setdefault("SERVER_IP", ip)
os.environ.setdefault("SERVER_PORT", str(port))


def open_browser():
    time.sleep(2)
    webbrowser.open(f"http://{ip}:{port}")


from django.core.management import execute_from_command_line
from file_manager.wsgi import application
from waitress import serve

# A packaged installation starts without a database.  Apply the bundled
# migrations before serving requests so the first completed upload cannot fail
# with "no such table" after the browser has sent the file.
execute_from_command_line(["manage.py", "migrate", "--noinput"])

# Do not open the browser until the upload database is ready.
threading.Thread(target=open_browser, daemon=True).start()

# Django's development server was previously started with --nothreading,
# which meant a file upload or download blocked every other client.  Waitress
# is a production WSGI server and its worker threads allow requests from
# multiple devices to be handled concurrently.
serve(application, host="0.0.0.0", port=port, threads=8)
