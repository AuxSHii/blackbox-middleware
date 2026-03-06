# BlackBox
![Uploading blackbox architecture.png…]()

BLACKBOX is a Django middleware that records failing HTTP requests
and allows replay and regression debugging.<img width="1366" height="768" alt="detailed ui" src="https://github.com/user-attachments/assets/77c65355-fc19-4c12-b3c8-08286542f1fb" />
<img width="1366" height="768" alt="bb timeline" src="https://github.com/user-attachments/assets/9845cc84-2c83-4dec-8233-47c42c9db9a1" />
<img width="1366" height="768" alt="bb diff" src="https://github.com/user-attachments/assets/cc809a5c-eb1e-44b5-8491-c19bd4e01abb" />
<img width="1366" height="768" alt="replay and assess UI" src="https://github.com/user-attachments/assets/490931a9-0caa-47a7-9a18-1cc87d3df10e" />
<img width="1366" height="768" alt="inspection ui" src="https://github.com/user-attachments/assets/453a731c-4abb-4249-8e97-228830509b8a" />

in a controlled db safe env.
configurable by user.

## Features

- Automatic request recording
- Replay engine
- Response diff detection
- Regression detection

## Installation

pip install clock-box

##through git

pip install git+https://github.com/AuxSHii/blackbox-middleware.git

## Usage

Add to INSTALLED_APPS:

    "blackbox"

Add middleware:

    "blackbox.middleware.BlackBoxMiddleware"

#confugure in project seettings

BLACKBOX={
   "ENABLED": True,               #master switch
   "RECORD_STATUS_CODES": [500],  # only record 500 i.e. server crashes
   "IGNORE_PATHS": ["/admin"],    # ignore admin panel = noise
   "MAX_REPLAY_PER_REQUEST": 3,      #keep only latest n replays i.e.5 here configured
   "DUPLICATE_IDENTICAL": True,       #deleeting spam replays
   "REPLAY_TTL_DAYS":14,
}
