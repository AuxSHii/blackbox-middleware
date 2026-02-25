from django.db.models import Count,Max #to do analytics stuff in sql [our req db!!]
from .models import RecordedRequest  

def failure_summary(queryset):
    """Analysyis recorded failures and return a digonostic summary"""
    queryset = RecordedRequest.objects.all()    #got all of our recordde requests in query set 

    if not queryset.exists():   #if queryset DNE plz dont crash ; but return an dict telling us there are no req or failures 
        return{
          "total_failure": 0,
          "by_status": {},
          "top_paths": [],
          "last_seen": None,
          "message": "No recorded failures yet"
        }
    
    # counting total failures
    total_failure = queryset.count()

    #GROUP by statuscodes
    status_breakdown = (              #status code : number of time it occur  -> 500 : 4
         queryset.values("response_status") #  from our rec req =queryset group by response status
         .annotate(count=Count("id"))    #for every group{each status code} COUNT - how many row exists ok? - count by id = count how many id are there cuz if id exist row exist as every req has id [id is unique also!!]     
         .order_by("-count")  # sort desc order of the counts so freq falure appear first!!!  as more count = more req = more ffailures
    )

    #GROUP by status
    by_status = {row["response_status"]: row["count"] for row in status_breakdown}

    #most FREQUESNTLY failing paths
    path_breakdown = (
         queryset.values("path")   # select path from rec req=queryset
         .annotate(count=Count("id"))  # for every group of a perticular path => count how many they are by id 
         .order_by("-count")[:5]      #now order them decending order of count so more failing paths appear fisrst ok?
    )                                 #only take the FRST 5 REZULTSS

    top_paths = [(row["path"], row["count"]) for row in path_breakdown]

    #last failure timestamp

    last_seen = queryset.aggregate(last=Max("timestamp")) ["last"]


    return{
       "total_failures": total_failure,
       "by_status": by_status,
       "top_paths": top_paths,
       "last_seen": last_seen,
       "path_breakdown": path_breakdown
       
    }









    return
    