from django.contrib import admin
from django.urls import path

from file import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload/success/', views.upload_success, name='file_upload_success'),
    path('file-list/', views.file_list, name='file_list'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]
