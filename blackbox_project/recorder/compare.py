from django.test import Client
from .models import RecordedRequest
import json




def compare_replay(record  , replay_response):
    """ 
    compare REPLAYED response with orininal RECORDED response
    DOES NOT RE RUN REPLAY JUST COMPARE RESULT
    
    """

    
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
