from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['project_name', 'public', ]
        lables = {
            'project_name': _('project name'),
            'public': _('public'),
        }


class ZoneForm(forms.ModelForm):
    class Meta:
        model = models.Zone
        fields = ['name', 'lenght', 'width', 'public']


class PlantDropdownForm(forms.ModelForm):
    class Meta:
        model = models.ZonePlant
        fields = ['plant']


class ZonePlantForm(forms.ModelForm):
    class Meta:
        model = models.ZonePlant
        fields = ['plant', 'color', 'qty', 'blooming_period', 'price', 'zone']
        widgets = {
            'plant': forms.HiddenInput(),
            'zone': forms.HiddenInput(),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'season']