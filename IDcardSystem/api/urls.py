from django.urls import path
from . import views


urlpatterns = [
    path('persons/', views.persons),
    path('add_person/', views.add_person),
    path('delete_person/', views.delete_person),
    path('update_person/', views.update_person),
    path('search_person/', views.search_person),

    path('get_provinces/', views.get_provinces),
    path('get_cities/', views.get_cities),
    path('get_ethnics/', views.get_ethnics),
]
