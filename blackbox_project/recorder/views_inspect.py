from django.shortcuts import render,redirect
from .models import RecordedRequest
from .analysis import failure_summary
from .filter import last_minutes
from django.shortcuts import get_object_or_404 
from django.views.decorators.http import require_POST
from recorder.compare import compare_replay
from recorder.replay import replay_request

@require_POST
def replay_from_ui(request , pk):
    """
    trigger the replay from inspection Ui
    """    
    #fetch the recorded request by the primary key = id
    record = get_object_or_404(RecordedRequest, pk=pk)
                                           # remember stored req = record = user's req+ OG response codes and body both sotred
    # replaying it using replay enegine      replaying a perticular request and storing the new response = status code+ body
    replay_response = replay_request(record)

    #compare original vs replayed   by calling replaly engine with that perticular req and replay respnse it gave
    result = compare_replay(record , replay_response)

    #temprorly store that result in our sessionnn to display
    request.session["bb_last_replay"] = result

    #redirect back to the same detail page
    return redirect("bb_request_detail", pk=pk)






#fxn for details of certain recorded request to display it
def request_detail(request , pk):
    #detailed display for a single captured req.
   
   record = get_object_or_404(RecordedRequest, pk=pk)
   
   #
   replay_result = request.session.pop("bb_last_replay", None)

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
       "replay_result": replay_result,
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
    