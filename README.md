WHAT IS BLACKBOX?  v1 -> RECORDING + REPLAY + COMPARISON  NOW ADDED DRAFT INSPECTION DASHBOARD with analysis
BLACKBOX is a django middleware that records failing HTTP requests and lets the user replay them as they originally happened.

like a FLIGHT RECORDER for backend


It Automatically Records (configurable)

HTTP method (GET, POST, etc.)
URL path + query string
Important headers
Raw request body
Parsed JSON body (if applicable)
Client IP
Timestamp
Response status + body (if available)

Even captures unhandled exceptions (server crashes)


# Replay Any Recorded Request
   You can replay a request exactly as the user sent it:

       from recorder.utils import replay_request

       replay_request(1)
BLACKBOX reconstructs:
  Original headers
  Original payload (raw or JSON)
  Exact URL
  Same request method
# Compare Original vs Replay Behavior

  from recorder.utils import compare_with_replay

   compare_with_replay(1)


Example Output:

 {
   'status_match': True,
   'body_match': False,
   'original_status': 500,
   'replay_status': 500,
   'notes': 'Same failure, logic changed.'
}
This helps detect:


1.Regression
2.Silent behavior changes
3.Incomplete fixes
 
 
 How It Works (Architecture)


Incoming Request
      ↓
BLACKBOX Middleware
      ↓
If Failure → Snapshot Saved to DB
      ↓
Can Replays Snapshot Later
      ↓
System Reconstructs Original Request
      ↓
Compare Old vs New Behavior



 Installation (Inside a Django Project)
1️.. Add App
Add recorder to:

INSTALLED_APPS = [
    ...
    "recorder",
]
2..   Register Middleware (IMPORTANT: near bottom)

MIDDLEWARE = [
    ...
    "recorder.middleware.BlackBoxMiddleware",
]
    !   Place it late so it can observe final responses/exceptions.
3️.   Configure BLACKBOX (optional)
In settings.py:

  BLACKBOX = {
     "ENABLED": True,
     "RECORD_STATUS_CODES": [500],
     "IGNORE_PATHS": ["/admin"],
}
