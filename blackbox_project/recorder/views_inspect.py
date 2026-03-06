from django.shortcuts import render,redirect
from .models import RecordedRequest
from .analysis import failure_summary
from .filter import last_minutes
from django.shortcuts import get_object_or_404 
from django.views.decorators.http import require_POST
from recorder.compare import compare_replay
from recorder.replay import replay_request
from django.core.paginator import Paginator
from django.db.models import Q
from recorder.diff_engine import generate_diff,generate_side_by_side
from .models import ReplayLog
from .retention import enforce_replay_attention,get_bb_setting
from django.utils import timezone
from .intelligence import analyze_change
from .stability import analyze_replay_stability

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
    
    #intell analysis
    OG_BODY = record.response_body_text or ""
    REPLAY_BODY= replay_response.content.decode() if replay_response.content else ""

    analysis = analyze_change(OG_BODY , REPLAY_BODY)
    #replay log cration and linking
    replay_log  = ReplayLog.objects.create(
        recorded_request = record,
        status_before = result["original_status"],
        status_after = result["replay_status"],
        body_changed = not result["body_match"],
        notes = result["notes"],

        #intell. fields
        lines_added = analysis["lines_added"],
        lines_removed = analysis["lines_removed"],
        size_before = analysis["size_before"],
        size_after = analysis["size_after"],
        keys_changed = analysis["keys_changed"],
        change_score = analysis["change_score"],

    )
    #choose what to reatin and what not    - after adding of requests
    enforce_replay_attention(record)

   
    
    #attaching diff infos
    diff_text = generate_diff(record.response_body_text , replay_response.content)

    side_by_side = generate_side_by_side(record.response_body_text , replay_response.content)

    result["diff_text"] = diff_text    # adding a unifieddiff
    result["diff_table"] = side_by_side  #adding lsit of lines of og and replay response to result
    
    #storing intell data in resut to pass it to templates
    result["intelligence"] = {
    "change_score": replay_log.change_score,
    "lines_added": replay_log.lines_added,
    "lines_removed": replay_log.lines_removed,
    "size_before": replay_log.size_before,
    "size_after": replay_log.size_after,
    "keys_changed": replay_log.keys_changed,
    
}
    regression = result["regression"], 
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

   replay_history = record.replays.all().order_by("-replayed_at")

   stability = analyze_replay_stability(record)

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
       "original_response_body": record.response_body_text,
       "replay_result": replay_result,
       "replay_history": replay_history,
       "stability": stability,
    }
   return render(request , "recorder/request_detail.html" , context)    

#fxn for inspect dashboard


def inspect_dashboard(request):
    """BLACKBOX Inspection Dashboard with filtering + pagination"""

    queryset = RecordedRequest.objects.all().order_by("-timestamp")

 
    #  filteriiings
    
    method = request.GET.get("method")
    status = request.GET.get("status")
    path = request.GET.get("path")
    search = request.GET.get("search")

    if method:
        queryset = queryset.filter(method__iexact=method)

    if status:
        queryset = queryset.filter(response_status=status)

    if path:
        queryset = queryset.filter(path__icontains=path)

    if search:
        queryset = queryset.filter(
            Q(path__icontains=search) |
            Q(headers__icontains=search) |
            Q(body_raw__icontains=search)
        )

  
    #  PAGINATION 
    
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

   
    #  ANALYTICS 
    analytics = failure_summary(RecordedRequest.objects.all())

    
    # CONTEXT 
    
    context = {
        "total": queryset.count(),
        "analytics": analytics,
        "page_obj": page_obj,
        "filters": {
            "method": method or "",
            "status": status or "",
            "path": path or "",
            "search": search or "",
        }
    }

    return render(request, "recorder/inspect.html", context)
