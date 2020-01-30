from django.http import HttpResponse, HttpResponseRedirect
from pathlib import Path
from slugify import slugify

from django.conf import settings
from django.shortcuts import render, redirect
from .forms import DocumentForm


from django.http import FileResponse


# Imaginary function to handle an uploaded file.
from .test_file_converter import process_file as test_convert

# def upload_file(request):
#     template = 'converter_app/upload.html'
#     response = HttpResponse()
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#
#             test_convert(request.FILES['file'], response)
#             return response
#             # return HttpResponseRedirect('/success/')
#     else:
#         form = DocumentForm()
#
#     context = {'form': form,
#                'response': response}
#     return render(request, template, context)
#
# def download_result(request):
#     template = 'converter_app/download.html'
#     success_link = "Here some chunk of success"
#
#     context = {
#         'success_link': success_link
#     }
#     return render(request, template, context)

def home(request):
    template = 'converter_app/base.html'
    context = {}
    return render(request, template, context)

def model_form_upload(request):
    template = 'converter_app/model_form_upload.html'

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file_data = form.save()
            file_link = Path(str(settings.MEDIA_ROOT) + '/'
                             + str(file_data.document))

            target_file = Path(str(settings.MEDIA_ROOT) + '/gift_converted/'
                               + f'GIFT_{file_link.parts[-1]}')
            target_file_name = slugify(target_file.parts[-1].replace('.txt', ''))

            test_convert(file_link, target_file)
            response = FileResponse(open(target_file, 'rb'))

            response["Content-Type"] = "text/json; charset=UTF-8"
            response["Content-Disposition"] = f'attachment; ' \
                                              f'filename={target_file_name}.txt'
            return response

    else:
        form = DocumentForm()

    context = {'form': form}

    return render(request, template, context)

