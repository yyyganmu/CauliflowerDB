from django import forms
from django.core.exceptions import ValidationError
from appcaulie import models


class BootstrapCSS:
    """
    添加bootstrap样式，之后再有form想用bootstrap样式的话，继承这个类就可以了
    再继承forms.Modelform或者forms.Form
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


class GeneinfoModelForm(BootstrapCSS, forms.ModelForm):

    class Meta:
        model = models.Geneinfo
        fields = ['chromosome', 'start', 'end']
        widgets = {
            # 'chromosome': forms.TextInput(attrs={'class': 'form-control'})
            'chromosome': forms.TextInput,
            'start': forms.NumberInput,
            'end': forms.NumberInput,
        }

    def clean_block(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if start >= end:
            raise ValidationError('Block Error.')
        return start, end