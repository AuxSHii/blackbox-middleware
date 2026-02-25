from django.urls import path
from .views_inspect import inspect_dashboard,request_detail


urlpatterns = [
    path('inspect/' , inspect_dashboard , name='blackbox-inspect'),
    path('inspect/<int:record_id>/' , request_detail , name='bb_request_detail'),
]