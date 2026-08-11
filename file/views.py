import os
import signal
import socket
from mimetypes import guess_type
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from file.forms import FileUploadForm


def get_local_ip():
    """
    Returns the machine's LAN IP (e.g. 192.168.x.x or 10.x.x.x).
    Falls back to 127.0.0.1 if nothing is found.
    Env vars SERVER_IP / SERVER_PORT still override everything.
    """
    env_ip = os.environ.get('SERVER_IP')
    if env_ip:
        return env_ip

    try:
        # Connect to an external address (doesn't actually send data)
        # so the OS picks the right outgoing interface automatically.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        pass

    # Fallback: iterate all interfaces
    try:
        hostname = socket.gethostname()
        addrs = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for addr in addrs:
            ip = addr[4][0]
            if not ip.startswith('127.'):
                return ip
    except Exception:
        pass

    return '127.0.0.1'


def upload_file(request):
    if request.method == 'POST':
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({'message': 'File uploaded successfully'}, status=201)
        else:
            return JsonResponse({'error': str(form.errors)}, status=400)
    else:
        form = FileUploadForm()
    return render(request, 'file/upload.html', {'form': form})


def upload_success(request):
    return render(request, 'file/upload_success.html')


def file_list(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()

    upload_dir = settings.MEDIA_ROOT

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    files = os.listdir(upload_dir)

    return render(request, 'file/file_list.html', {'form': form, 'files': files})


def download_file(request, filename):
    """Stream an uploaded file while preserving its original download name."""
    upload_dir = Path(settings.MEDIA_ROOT).resolve()
    file_path = (upload_dir / filename).resolve()

    # Do not allow a crafted URL to escape the upload directory.
    if upload_dir not in file_path.parents or not file_path.is_file():
        raise Http404('File not found')

    content_type, _ = guess_type(file_path.name)
    return FileResponse(
        file_path.open('rb'),
        as_attachment=True,
        filename=file_path.name,
        content_type=content_type or 'application/octet-stream',
    )


def home(request):
    ip = get_local_ip()
    port = os.environ.get('SERVER_PORT', '8000')
    server_url = f"http://{ip}:{port}"
    return render(request, 'file/home.html', {'server_url': server_url})


def shutdown(request):
    os.kill(os.getpid(), signal.SIGTERM)
    return HttpResponse("Server shutting down...")
