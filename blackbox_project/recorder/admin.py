from django.contrib import admin
from .models import RecordedRequest  
from .models import ReplayLog
from .models import MockItem

   #my recordedreq model
#registerd our recorder model here
@admin.register(RecordedRequest)


class RecordedRequestAdmin(admin.ModelAdmin):
    list_display =("method" , "path" , "response_status" , "timestamp", "tag" , "id")
    search_fields = ("path" , "tag" )
    list_filter = ("method" , "response_status" , "timestamp" )


#replylog admimn
    
@admin.register(ReplayLog)
class ReplayLogAdmin(admin.ModelAdmin):
    list_display = ("recorded_request",
                    "status_before",
                    "status_after",
                    "change_score",
                    "lines_added",
                    "lines_removed",
                    )
    list_filter = ("change_score", "status_before", "status_after" )

    search_fields = ("recorded_request__path" ,)

@admin.register(MockItem)
class MockItemAdmin(admin.ModelAdmin):
    list_display = ("name", "id" )
    search_fields= ("name",)