from django.urls import path
from .views import home , update_database_from_csv

urlpatterns = [
    path('', home),
    path('update',update_database_from_csv, name='update'),
]
