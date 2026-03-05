from django.urls import path
from .views import boom
from .views import delete_mock_item

urlpatterns =[
    path("boom/" , boom , name='boom'),

    path("mock/delete/<int:item_id>/" , delete_mock_item ),

]
