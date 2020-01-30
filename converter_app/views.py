from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import DocumentForm

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


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'converter_app/model_form_upload.html', {
        'form': form
    })