from django.shortcuts import render
from .models import MockItem

from django.http import JsonResponse

def boom(request):
    #this is an intentional crash/problematic point
    x = 1/0
    return JsonResponse({"ok": True})


#mock delete view to test db rollback changes in transaction feature

def delete_mock_item(request , item_id):
    
    obj = MockItem.objects.get(id=item_id)
    obj.delete()

    return JsonResponse({
        "status": "deleted",
        "id": item_id,

    })