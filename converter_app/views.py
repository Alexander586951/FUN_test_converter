from pathlib import Path
from slugify import slugify

from django.conf import settings
from django.shortcuts import render
from .forms import DocumentForm

from django.http import FileResponse, HttpResponse

# Imaginary function to handle an uploaded file.
from .test_file_converter import process_file as test_convert


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

