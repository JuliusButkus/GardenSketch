from typing import Any
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

# project views below

class MyProjectsView(LoginRequiredMixin, generic.ListView):
    model = models.Project
    template_name = "gardenplaner/my_projects.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class CreateProjectView(LoginRequiredMixin, generic.View):
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
    
    

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = models.Project
    template_name = "gardenplaner/project_detail.html"
    context_object_name = "project" #naudota anksciau sename projekte

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zones'] = models.Zone.objects.filter(project=self.object)
        return context
    
    def get_initial(self)->dict[str, Any]:
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial
       
    
    def test_func(self) -> bool | None:
        self.object = self.get_object()
        return self.request.user == self.object.user


class CreateZoneView(LoginRequiredMixin, generic.View):
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
    

class ZoneDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Zone
    template_name = 'gardenplaner/zone_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plants_dropdown_form'] = forms.PlantDropdownForm
        return context


class AddZonePlantView(LoginRequiredMixin, generic.View):
    template_name = 'gardenplaner/add_plant.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        context['zone'] = get_object_or_404(models.Zone, pk=self.kwargs['zone_id'])
        context['plant'] = get_object_or_404(models.Plant, pk=self.request.GET.get('plant'))
        context['form'] = forms.ZonePlantForm(initial=self.get_initial())
        context['form'].fields['color'].queryset = models.Color.objects.filter(plants=self.request.GET.get('plant'))
        return context
    
    def get_initial(self) -> dict[str, Any]:
        initial = {}
        initial['zone'] = self.kwargs['zone_id']
        initial['plant'] = self.request.GET.get('plant')
        return initial
    
    def get(self, request, zone_id):
        context = self.get_context_data(zone_id=zone_id)
        return render(request, self.template_name, context)
   
    def post(self, request, zone_id):
        zone = get_object_or_404(models.Zone, pk=zone_id)
        form = forms.ZonePlantForm(request.POST)  
        if form.is_valid():
            zone_plant = form.save(commit=False)
            zone_plant.zone = zone
            zone_plant.save()
            return redirect('zone_detail', pk=zone_id)
        else:
            context = self.get_context_data(zone_id=zone_id)
            return render(request, self.template_name, context)
    
    
class AddPhotoView(LoginRequiredMixin, generic.View):  
    template_name = "gardenplaner/add_photo.html" 

    def get(self, request, zone_id):
        zone = get_object_or_404(models.Zone, pk=zone_id)
        photos = models.Photo.objects.filter(zone=zone).all()
        photo_form = forms.PhotoForm()  
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


class UpdateZoneView(LoginRequiredMixin, generic.UpdateView):
    model = models.Zone
    form_class = forms.ZoneForm
    template_name = 'gardenplaner/update_zone.html'

    def get_success_url(self):
        return reverse_lazy('zone_detail', kwargs={'pk': self.object.id})
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)