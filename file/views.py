import os

from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from file.forms import FileUploadForm


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({'message': 'File uploaded successfully'}, status=201)
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
            return redirect('file_list')  # Redirect to the same page after upload
    else:
        form = FileUploadForm()

    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    files = os.listdir(upload_dir)

    return render(request, 'file/file_list.html', {'form': form, 'files': files})


def download_file(request, filename):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)


def home(request):
    ip = os.environ.get('SERVER_IP', '127.0.0.1')
    port = os.environ.get('SERVER_PORT', '8000')
    server_url = f"http://{ip}:{port}"
    return render(request, 'file/home.html', {'server_url': server_url})