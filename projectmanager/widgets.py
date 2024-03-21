# widgets.py
from django import forms

class MultiTagWidget(forms.TextInput):
    def __init__(self, delimiter=',', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delimiter = delimiter

    def value_from_datadict(self, data, files, name):
        value = data.get(name, '')
        return value.split(self.delimiter)
