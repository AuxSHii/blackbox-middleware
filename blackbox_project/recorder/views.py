from django.shortcuts import render

from django.http import JsonResponse

def boom(request):
    #this is an intentional crash/problematic point
    x = 1/0
    return JsonResponse({"ok": True})
