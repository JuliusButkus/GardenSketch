from typing import Any
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from . import models, forms
from django.views.decorators.csrf import csrf_protect


def delete_project_view(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('my_projects')
    return render(request, 'gardenplaner/delete_project.html', {'project': project})

def index(request: HttpRequest):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
    }
    return render(request, 'gardenplaner/index.html', context)

class TypeListView(generic.ListView):
    model = models.Type
    template_name = "gardenplaner/plant_types.html"
    context_object_name = "type_list"
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = True
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(name_en__icontains=query) | 
                Q(name_lt__icontains=query)  
            )
        return queryset
    

class PlantListView(generic.ListView):
    model = models.Plant
    template_name = "gardenplaner/plant_list.html"
    context_object_name = "plant_list"
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = True
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(name_en__icontains=query) | 
                Q(name_lt__icontains=query)  
            )
        return queryset   

# projekt views below

class MyProjectsView(generic.ListView):
    model = models.Project
    template_name = "gardenplaner/my_projects.html"
    # context_object_name = "gardenproject_list"
    paginate_by = 10


class CreateProjectView(generic.View):
    template_name = 'gardenplaner/create_project.html'

    def get(self, request, *args, **kwargs):
        form = forms.ProjectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  
            project.save()
            return redirect('project_detail', pk=project.pk)
        return render(request, self.template_name, {'form': form})
    

class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = "gardenplaner/project_detail.html"
    context_object_name = "project" #naudota anksciau sename projekte

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zones'] = models.Zone.objects.filter(project=self.object)
        return context


class CreateZoneView(generic.View):
    template_name = 'gardenplaner/create_zone.html'

    def get(self, request, project_id):
        project = get_object_or_404(models.Project, pk=project_id)
        zone_form = forms.ZoneForm()
        return render(request, self.template_name, {
            'zone_form': zone_form,
            'project': project
        })

    def post(self, request, project_id):
        project = get_object_or_404(models.Project, pk=project_id)
        zone_form = forms.ZoneForm(request.POST)

        if zone_form.is_valid():
            zone = zone_form.save(commit=False)
            zone.project = project
            zone.save()
            return redirect('zone_detail',  pk=project.id)

        return render(request, self.template_name, {
            'zone_form': zone_form,
            'project': project
        })
    

class ZoneDetailView(generic.DetailView):
    model = models.Zone
    template_name = 'gardenplaner/zone_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plants_dropdown_form'] = forms.PlantDropdownForm
        # context['selected_plants'] = models.ZonePlant.objects.filter(zone=self.object)
        # turetu teori6kai buti nereikalingi
        return context
    

class AddPlantView(generic.CreateView):
    model = models.ZonePlant
    form_class = forms.ZonePlantForm
    template_name = 'gardenplaner/add_plant.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['zone'] = get_object_or_404(models.Zone, pk=self.kwargs['zone_id'])
        context['plant'] = get_object_or_404(models.Plant, pk=self.request.GET.get('plant'))
        return context

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['zone'] = self.kwargs['zone_id']
        initial['plant'] = self.request.GET.get('plant')
        return initial
    
    def get_form(self, form_class: type[BaseModelForm] | None = ...) -> BaseModelForm:
        form = forms.ZonePlantForm(initial=self.get_initial())
        form.fields['color'].queryset = models.Color.objects.filter(plant=self.request.GET.get('plant'))
        return form

class AddPhotoView(generic.View):  
    template_name = "gardenplaner/add_photo.html" 

    def get(self, request, zone_id):
        zone = get_object_or_404(models.Zone, pk=zone_id)
        photos = models.Photo.objects.filter(zone=zone).all()
        photo_form = forms.PhotoForm()  # Use the correct form from your forms module
        context = {
            'zone': zone,
            'photos': photos,
            'photo_form': photo_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, zone_id):
        zone = get_object_or_404(models.Zone, pk=zone_id)
        photo_form = forms.PhotoForm(request.POST, request.FILES)  
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.zone = zone
            photo.save()
            return redirect('add_photo', zone_id=zone_id)
        else:
            photos = models.Photo.objects.filter(zone=zone).all()
            context = {
                'zone': zone,
                'photos': photos,
                'photo_form': photo_form,
            }
            return render(request, self.template_name, context)