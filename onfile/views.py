import csv
import io
import re
import xml.etree.ElementTree as ET

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import UploadFilesForm
from .helper import _process_file


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'


@login_required(login_url='/accounts/login/')
def process_csv(request):
    if "GET" == request.method:
        form = UploadFilesForm()
        return render(request, 'upload_csv.html', {'form': form})
    else:
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES['csv_file'].name.endswith('.csv') and \
                    request.FILES['xml_file'].name.endswith('.xml'):
                csv_file = request.FILES['csv_file'].read().decode('UTF-8')
                xml_file = request.FILES['xml_file']
                io_string = io.StringIO(csv_file)
                reader = csv.DictReader(io_string)

                processed_file = _process_file(reader, xml_file)
                
                with open('new_file.xml', 'rb') as f:
                    response = HttpResponse(f, content_type='text/xml')
                    response[
                        'Content-Disposition'] = 'attachment; filename = ' \
                                                    '"new_file.xml"'
                return response
            else:
                messages.warning(request, 'Please use correct files')
                form = UploadFilesForm()
                return render(request, 'upload_csv.html', {'form': form})

        else:
            form = UploadFilesForm()
            return render(request, 'upload_csv.html', {'form': form})
