from django.shortcuts import render
from .models import RecordedRequest
from .analysis import failure_summary
from .filter import last_minutes
from django.shortcuts import get_object_or_404 
#fxn for details of certain recorded request to display it
def request_detail(request , record_id):
    #detailed display for a single captured req.
   
   record = get_object_or_404(RecordedRequest, id=record_id)

   context = {
       "record": record,
       "headers": record.headers or {},
       "query": record.query_string,
       "body_raw": record.body_raw,
       "body_parsed": getattr(record , "body_parsed", None),   # ayy if the object=request  has a json pared body then give it to me if not then PLZ DONT CRASH instead return None 
       "method": record.method,
       "path": record.path,
       "timestamp": record.timestamp,
       "original_response_status": record.response_status,
       "original_response_body": record.response_body,
    }
   return render(request , "recorder/request_detail.html" , context)    

#fxn for inspect dashboard
def inspect_dashboard(request):
    """ friendy ispection dashboard for BLACKBOX [READ ONLY] """
#all record requests (latest first)
    queryset = RecordedRequest.objects.all().order_by("-timestamp")

    #activity in last 10 minute
    recent_queryset = last_minutes(queryset , 10)

    #use analytics alrready built
    analytics = failure_summary(queryset)

    context = {
        "total": queryset.count(),  #total number of requests
        "recent_count": recent_queryset.count(),  # recent req count of la st 10 min hard coded
        "analytics": analytics,   # giving analytics dict
        "latest": queryset[:10], #last 10 captured req

    }
    print("analytics data-" , analytics)

    return render(request , "recorder/inspect.html" , context)
    