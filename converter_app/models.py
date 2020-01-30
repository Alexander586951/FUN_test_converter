from django.db import models

class Document(models.Model):
    document = models.FileField(upload_to='documents/',
                                verbose_name='Выбрать файл')
    uploaded_at = models.DateTimeField(auto_now_add=True)