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
                io_string = io.StringIO(csv_file)
                reader = csv.DictReader(io_string)

                for fieldname in reader.fieldnames:
                    if result := re.match('hawb(s*)', fieldname, re.IGNORECASE):
                        name = result.group(0)

                        # collect hawbs to compare against hawb nodes in xml
                        # file
                        hawbs = {str(row[name]) for row in reader}
                        new_hawbs = []
                        for hawb in hawbs:
                            while len(hawb) < 11:
                                hawb = '0' + hawb
                            new_hawbs.append(hawb)

                xml_file = request.FILES['xml_file']
                parsed_xml = ET.parse(xml_file)
                parsed_xml_root = parsed_xml.getroot()
                parsed_list = parsed_xml_root.findall("ENTRY")

                for item in parsed_list:
                    if item.find("MANIFEST").find(
                            "HOUSE").text not in new_hawbs:
                        parsed_xml_root.remove(item)

                parsed_xml.write('new_file.xml', xml_declaration=True)
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
