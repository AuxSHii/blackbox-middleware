import json
import difflib

def normalize_body(body):
    #convt body - compararble str handle json,text safely
    if body is None:
        return ""
    
    #if djaango rep content = bytes

    if isinstance(body, bytes):  #is body an instanc eo f byte class
        body = body.decode("utf-8" , errors="ignore")  # if yes  then decode it into string
    #rety to pretty formst json
    try:
        parsed = json.loads(body)  #covt raw json body into py obj/dict
        return json.dumps(parsed , indent=2 , sort_keys=True)  #convt py obj to json and sorted in alphabetical order
    except Exception:
        return str(body)

def generate_diff(original_body , replay_body):
    # return a unified str btw og body and replay body

    original_text = normalize_body(original_body).splitlines() #list of line of og body
    replay_text = normalize_body(replay_body).splitlines()   #list of lines of replay body

     #now these lines of og and replay can be coompared and bein a diff

    diff = difflib.unified_diff(      #called unified lib methjod from difflib module on folllowing 
        original_text,
        replay_text,
        fromfile="original",
        tofile="replay",
        lineterm=""
    )


    return "/n".join(diff)   #join iterator returnd by unifiediff to str dor displaying

def generate_side_by_side(original_body , replay_body):
    #prod structure row for html rendering 
    original_text = normalize_body(original_body).splitlines()
    replay_text = normalize_body(replay_body).splitlines()

    matcher = difflib.SequenceMatcher(None, original_text , replay_text)
    #compare these 2 texts 
    rows = []  # prepare output container

    for opcode, i1 ,i2 ,j1 , j2 in matcher.get_opcodes():
        if opcode == "equal":
            for i in range(i2 - i1):
                rows.append(("same", original_text[i1+i] , replay_text[j1+i]))

        elif opcode == "replace":
            for i in range(max(i2 - i1, j2 - j1)):
                o = original_text[i1+i] if i1 + i < j2 else ""
                r = replay_text[j1+i] if j1 + i < j2 else ""
                rows.append(("changed" , o , r))

        elif opcode == "delete":
            for i in range(i1 , i2):
                rows.append(("removed", original_text[i] , ""))

        elif opcode == "insert":
            for i in range (j1 , j2):
                rows.append(("added" , "" , replay_text[i]))
    return rows
    
    