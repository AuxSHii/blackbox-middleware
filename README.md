# BlackBox

BLACKBOX is a Django middleware that records failing HTTP requests
and allows replay and regression debugging.
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