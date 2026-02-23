from django.contrib import admin
from .models import RecordedRequest     #my recordedreq model

#registerd our recorder model here
@admin.register(RecordedRequest)

class RecordedRequestAdmin(admin.ModelAdmin):
    list_display =("method" , "path" , "response_status" , "timestamp", "tag" , "id")
    search_fields = ("path" , "tag" )
    list_filter = ("method" , "response_status" , "timestamp" )


