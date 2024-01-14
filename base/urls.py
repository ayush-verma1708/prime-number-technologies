from django.urls import path
from .views import home , update_database_from_csv , search_results

urlpatterns = [
    path('', home),
    path('update',update_database_from_csv, name='update'),
    path('search/', search_results, name='search_results'),
]
