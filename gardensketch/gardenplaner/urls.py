from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('type_list/', views.TypeListView.as_view(), name='plant_types'),
    path('plant_list/', views.PlantListView.as_view(), name='plant_list'),

    path('projects/', views.MyProjectsView.as_view(), name='my_projects'),
    path('projects/create/', views.CreateProjectView.as_view(), name='create_project'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/delete/', views.DeleteProjectView.as_view(), name='delete_project'),
    path('project/<int:project_id>/zone/create/', views.CreateZoneView.as_view(), name='create_zone'),
    path('project/<int:project_id>/zone/<int:pk>/delete/', views.DeleteZoneView.as_view(), name='delete_zone'),


    path('zone/<int:pk>/', views.ZoneDetailView.as_view(), name='zone_detail'),
    path('zone/<int:zone_id>/plant/add/', views.AddZonePlantView.as_view(), name='add_plant'),
    path('add_photo/<int:zone_id>/', views.AddPhotoView.as_view(), name='add_photo'),
    
    path('zone/<int:pk>/update/', views.UpdateZoneView.as_view(), name='update_zone'),
    path('zone/<int:zone_id>/plant/<int:pk>/delete/', views.DeleteZonePlantView.as_view(), name='delete_zone_plant'),
    path('zone/<int:zone_id>/photo/<int:pk>/delete/', views.DeleteZonePhotoView.as_view(), name='delete_zone_photo'),

    
]
