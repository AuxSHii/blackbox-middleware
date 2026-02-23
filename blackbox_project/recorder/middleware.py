import json
from .models import RecordedRequest #MY RECORDING REQ MODEL
from .config import BlackBoxSettings #heres the config settings {default + user defined (if esists)}



class BlackBoxMiddleware:
    """
    Capturing  request + response cycle automatically.
    """

    def __init__(self, get_response): # constructor: when BLACKBOx starts
        self.get_response = get_response
        self.settings = BlackBoxSettings()  # user def+default confi setting for blackbox
                                            #self.settings = our config object
    def __call__(self, request):
    
    # If BLACKBOX disabled → do nothing
        if not self.settings.ENABLED:          #not enabled
           return self.get_response(request)  #give control to django

    # Ignore noisy paths immediately
        for ignored_path in self.settings.IGNORE_PATHS:   # for every IGNORED PATH
            if request.path.startswith(ignored_path):   #check if the request has the IGNORED PATH
               return self.get_response(request)        #if yes for any iteration - give control to django

        try:                                       
        # Let Django process request first            
            response = self.get_response(request)          #all green-flag path here give control to django]VIEWS
                                                                 
        except Exception as exc:                             #an exception/failure where no response was returned to BLACKBOX
        # onllyyyy!!! NOW extract data (because crash happened)
            request_data = self.extract_request_data(request)     
            self.record_exception_event(request, exc, request_data)    #manually record the exception event 
            raise                                       # to raise exception - let django show error and control
                                                   
    # Decide if this response should be recorded
        if response.status_code in self.settings.RECORD_STATUS_CODES:
             request_data = self.extract_request_data(request)
             self.record_event(request, response, request_data)
        return response

    #--------------------------------------------
    #function to record exceptional events i.e. to record both 
    # bad response (configured) + actual crashes(exceptions)
    #at actual cases django seems to have an internal error handlojg system so it wont give the response back it will iternaly pause there

    # ------------------------------
    # helper  fxn to extract data from req. b4 mutation
    def extract_request_data(self, request):
        """capturing raw req"""
        
        try:
            raw_body = request.body.decode("utf-8")
            parsed_body = json.loads(raw_body) if raw_body else None 
        except Exception:
            raw_body = "<binary>"
            parsed_body = None

        #headers for repaly fxn and django clinet fxn  parsing
            
        headers = {
            "Content-Type": request.headers.get("Content-Type"),
            "User-Agent": request.headers.get("User-Agent"),
            "Accept": request.headers.get("Accept"),
        }

        #returnign structured snapshot like json body+rawbody, headers etc
        return{
        "method":request.method,
        "path": request.path,
        #structured query parameters (replay frinedly)
        "query_string": request.META.get("QUERY_STRING" , ""),   
        #raw body preserved
        "body_raw": raw_body ,
        #now for json parsed body
        "body_parsed" : parsed_body,
        "ip" : request.META.get("REMOTE_ADDR" , "127.0.0.1"), #fallback for test client rplay  aplaceholder ip for  
        #minimal headers_(less in size and less noise)
        "headers": headers,
        #this is user context
        "user": str(request.user) if request.user.is_authenticated else "anonymous" ,



        }


    # ------------------------------
   # recording event - to decide if save the req data or not i.e. is it RED-FLAG?
    def record_event(self, request, response, request_data):
        """Persist the recorded request."""

        # Only store problematic responses (avoid anything else)
        #IS BLACKBOX turned off?
        if not self.settings.ENABLED:
            return
        #IGNORE UNWANTED PATHS LIKE /admin , /static
        if request.path.startswith(tuple(self.settings.IGNORE_PATHS)):   #if the path of our request have admin or static or any othe ruser defineed path then DONT RECORD THAT REQUEST 
            return
        #Recording only SPECEFIC CODES 
        if response.status_code not in self.settings.RECORD_STATUS_CODES:
            return       # record those req with codes already configured

        try:       #what the server returned for thosee rerequests
            response_body = response.content.decode("utf-8") # read what server returned  
            response_body = json.loads(response_body) if response_body else None # convt json resp to py dict.
        except Exception:
            response_body = None

          # SAVING RECORDED REQUEST (probelematic one) to OUR MODEL DB (RecordedRequest) class      
        RecordedRequest.objects.create(
            method=request_data["method"],
            path=request_data["path"],
            query_string=request_data.get("query_string" , ""),
            headers=request_data.get("headers" , {}),
            body_raw=request_data.get("body_raw"),
            body_parsed=request_data.get("body_parsed"),
            response_status=response.status_code,
            response_body=response_body,
            ip_address=request_data.get("ip" , "127.0.0.1"), # here when saving recorded req t our db the ip will be either user fetched ip or the placeholder used in my replay fxn
            tag="auto-captured",
        )
        #populating the field using the [request_data] and [response]S


        #important note: while registering blackbox into your mains settings
        #register it near the bottom so it doesnt miss things like authentications or any exception handling