from django.test import Client
from .models import RecordedRequest
import json
from urllib.parse import urlencode

#simple class to simulate a response when view crashe i.e. exceptions happen = when django internal error resolution takes over
class FakeResponse:
    def __init__(self , status_code , content=b""):
        self.status_code = status_code
        self.content =content


#fxn for replaying req from our db through id
def replay_request(record_id):
    """wil replay a recorded request by ID using django's test client 
     return RESPONSE OBJ if successfull or print the exception if it crashes
    
    """   #that primary key field=id , that django provides to mdoels unless I DISABLE IT which I DID NOT..
    try:                 #record=fetching the req we wanna replay with the help of id
        record = RecordedRequest.objects.get(id=record_id)
    except RecordedRequest.DoesNotExist:
        print("no recorded request found with id:" , record_id)
        return None

    #will initialize django test client now
    client = Client()

    #prepare the headers
    headers = record.headers or {}
    #django test client [requires special format for http_headers] 
    http_headers = {f"HTTP_{k.upper().replace('-', '_')}": v for k, v in headers.items()}

    #overridin defult testserver host
    http_headers["HTTP_HOST"] = "127.0.0.1"

    #prepare method , path and body- prefer parsed json if exist , else raw
    method = record.method.lower()
    path = record.path
    #use stored query_string (string or dict) 
    query_string = record.query_string or ""
    if query_string:
        if isinstance(query_string ,dict):   #checkin if stored query is a py dict - through urlencode covt dic to URL params properly    like from dict: {"tag": ["x" , "y"]} to a URL { ?tag=x&tag=y }
            path = f"{path}?{urlencode(query_string, doseq=True)}"       #merging path + query_string     
        else:      #if stroed query_string is laready a string then append it as it is with the path..
            path = f"{path}?{query_string}"

    #body: prefer parsed json if exists ,otherwise fall back to raw
    body = record.body_parsed if getattr(record , "body_parsed" , None) else record.body_raw
    #save body_parsed into body only if the attribute body_parsed exists in object record ..ie. if body parsed exist

    
    #dispatching thwe request
    #generic() = will allow arb. HTTP methods (GET ,POST , PUT) 
    #sends modified/reconstructed body and headers
    #BLACKBOX still active at this point to record again - to compare new repnses with OG
    
    try:    #try passing client testsever with our request of certain id , orint status and return response / if no response given out then rasie exception in which call that fakeresponse fxn that will give response 500 
        response = client.generic(method.upper() , path , data=body , content_type=headers.get("Content-Type"), **http_headers)

        print("REPLAY FINISHED STATUS:", response.status_code)
        return response
    except Exception as exc:
        print(f"Exception during replay of record {record_id}: {exc}")
        #return a fake response calling code can inspect status
        response = FakeResponse(status_code=500 , content=b"View Raised Exception")

    print("REPLAY FINISHED STATUS:" ,  response.status_code)
    return response 



    #FXN TO COMPARE THE OLD RESPONSE AND NEW REPLAYED RESPONSE

def compare_replay(record_id , replay_response):
    """ 
    compare REPLAYED response with orininal RECORDED response
    DOES NOT RE RUN REPLAY JUST COMPARE RESULT
    
    """

    try:
        record = RecordedRequest.objects.get(id=record_id)
    except RecordedRequest.DoesNotExist:
        print("No recorded request found with id:" , record_id)
        return None
    
    #orginal data from db
    original_status = record.response_status
    original_body = record.response_body
    #REPLAY DATA
    replay_status = replay_response.status_code

    try:
        replay_body = json.loads(replay_response.content.decode("utf-8"))
    except Exception:
        replay_body = replay_response.content.decode("utf-8" , errors="ignore")


   
    #COMPARISON
    status_match = original_status == replay_status
    body_match = original_body == replay_body


    #RESULT
    result = {
        "status_match": status_match,
        "body_match" : body_match,
        "original_status": original_status,
        "replay_status": replay_status,
        "original_body": original_body,
        "replay_body" : replay_body,
    }


    #OUR HUMAN ISNIGHTSS..
    if status_match and body_match:    # if both true
        result["notes"] = "Replay behaved ecaxtly the SAME."
    elif not status_match and replay_status < 500:  #status match was fasle but replay_status is less then 500
        result["notes"] = "status improved - bug likely FIXED."
    elif not status_match:                    # status_match was false but still with RED FLAG CODE
        result["notes"] = "status changed - behaviour DIFFERENT."
    else:                  #status match is true but bodymatch is false
        result["notes"] = "SAME status but DIFFERENT body-logic changed."




    print("COMPARISON RESULT:" , result["notes"])
    return result          

    