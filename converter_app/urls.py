from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

app_name = 'converter_app'
urlpatterns = [
    path('', views.model_form_upload, name='upload_form'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)