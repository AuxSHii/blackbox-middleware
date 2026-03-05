#for diff summary

import json
import difflib

def safe_to_text(body):
    #normalize body[str,bts;dicts,None] into clean string

    if body is None:
        return ""
    if isinstance(body ,bytes):
        body = body.decode("utf-8" , errors="ignore")

    if isinstance(body , (list , dict)):
        try:
            return json.dumps(body , indent=2, sort_keys=True)  #serialize obj into a jsoon formated string
        except Exception: 
            return str(body)
        
    return str(body)
        

def extract_json_keys(text):
    #try to extract top lvl json keys into a SET

    try:
        parsed = json.loads(text)    #desrilize str[json doc] into a py obj (dict,list)
        if isinstance(parsed , dict):    #if pared was dict  
            return set(parsed.keys())     #returning a set of all the keys [item of ] parsed
        
    except Exception:
        pass


    return set()


def analyze_change(original_body , replay_body):
    #return a lite intell summary btw 2 bodies

    original_text = safe_to_text(original_body)   #string [text]
    replay_text = safe_to_text(replay_body)   #returns a string[text]
    
    original_lines = original_text.splitlines()   #store og text line by line to use diff on it
    replay_lines = replay_text.splitlines()
    
    #line differnece

    diff = list(difflib.ndiff(original_lines, replay_lines))

    lines_added = sum(1 for line in diff if line.startswith("+"))    #from diff[+lines added] = number of th0ose
    lines_removed = sum(1 for line in diff if line.startswith("-"))   #from diff [-lines removed] = number of thsoe
    
    #size differnece

    size_before = len(original_text.encode("utf-8"))
    size_after = len(replay_text.encode("utf-8"))

    #json key differnece

    original_keys = extract_json_keys(original_text)
    replay_keys = extract_json_keys(replay_text)

    keys_changed = list(original_keys.symmetric_difference(replay_keys))  #returns a set of changed/different keys

    #score of changes

    total_change = lines_added + lines_removed

    #analysis on total change[loose]

    if total_change == 0:
        change_score = "LOW"

    elif total_change < 10:
        change_score = "MEDIUM"

    else:
        change_score = "HIGH"


    return{
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "size_before": size_before,
        "size_after": size_after,
        "keys_changed": keys_changed,
        "change_score": change_score
    } 