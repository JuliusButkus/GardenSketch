from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('type_list/', views.TypeListView.as_view(), name='plant_types'),
    path('plant_list/', views.PlantListView.as_view(), name='plant_list'),

    path('projects/', views.MyProjectsView.as_view(), name='my_projects'),
    # path('create_project/', views.CreateGardenProjectView.as_view(), name='create_project'),
    # path('gardenproject_detail/<int:pk>/', views.GardenProjectDetailView.as_view(), name='gardenproject_detail'),
    # path('delete_project/<int:pk>/', views.delete_project_view, name='delete_project'),
    # path('confirm_delete_project/<int:pk>/', views.confirm_delete_project_view, name='confirm_delete_project'),
    # path('zone_detail/<int:pk>/', views.ZoneDetailView.as_view(), name='zone_detail'),
    # path('create_zone/<int:project_id>/', views.CreateZoneView.as_view(), name='create_zone'),
    # path('zone/<int:zone_id>/plant/add/', views.AddPlantView.as_view(), name='add_plant'),
    # path('add_photo/<int:zone_id>/', views.AddPhotoView.as_view(), name='add_photo'),
    
]
