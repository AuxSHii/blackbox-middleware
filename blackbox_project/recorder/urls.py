from django.urls import path
from .views import boom

urlpatterns =[
    path("boom/" , boom , name='boom'),
 
]