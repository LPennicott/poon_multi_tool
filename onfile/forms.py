from django import forms


class UploadFilesForm(forms.Form):

    csv_file = forms.FileField()
    xml_file = forms.FileField()
