from django.urls import path
from .views_inspect import inspect_dashboard,request_detail,replay_from_ui


urlpatterns = [
    path('inspect/' , inspect_dashboard , name='blackbox-inspect'),
    path('inspect/<int:pk>/' , request_detail , name='bb_request_detail'),
    path('inspect/<int:pk>/reply' , replay_from_ui , name='bb_replay'),
   
]