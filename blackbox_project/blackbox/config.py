from django.conf import settings

# class to read blackbox config from settings.py (her majesty)
 

class BlackBoxSettings:
    """
    reads user-defined BLACKBOX settings from django settings.py
    & provide defaults if not configured
    """
    #here i defined the default configs
    DEFAULTS ={
        "RECORD_STATUS_CODES":[500], #ONLY RECORD SERVER ERRORS BYDEFAULT ..which http errors to save
        "IGNORE_PATHS": ["/admin" , "/static"], # those url paths blackbox don't careabout 
        "ENABLED": True, #masterswitch to turn it ON or OFF
    }
       #exc once at server startup
    def __init__(self):
        user_settings  = getattr(settings , "BLACKBOX", {} ) #read uesr configs in settings.py ,  if exists then return it i not then return empty{}
        self.config = {**self.DEFAULTS, **user_settings}   #merging ouur defaults with user settings
# merging - start with default then overwrite whatever user provided
    def __getattr__(self , item):
        try:
           return self.config[item]
        except KeyError:
            raise AttributeError(f"Invalid BlackBox setting: {item} ")  
            
        