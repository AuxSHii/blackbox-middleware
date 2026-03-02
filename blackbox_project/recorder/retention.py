from django.conf import settings
from .models import ReplayLog


def get_bb_setting(key,default=None):    #a safe accessor for blackbox(bb) settings
    return getattr(settings , "BLACKBOX" , {}).get(key , default)   # EXTRACTING KEY ADN DEFAULT FROM THE blackbos config settings from settings.py


def enforce_replay_attention(record):
    #apply bb's replay retentiion rules

    max_keep = get_bb_setting("MAX_REPLAY_PER_REQUEST" , 5)
    delete_identical = get_bb_setting("DUPLICATE_IDENTICAL" , True)

    replays = ReplayLog.objects.filter(
        recorded_request=record   #filtering condn = check if OG REQ == recorded req in replay log
    ).order_by("-replayed_at")

    #triiming older replays         now replays = 

    if replays.count() > max_keep: #if cout of replay log req gtr then configd limit of requests
        for old in replays[max_keep:]:  
            old.delete()
    
    #2. removing identical replays [spam]
                    #if replay_identical settings is true and count of replays more thenn 2
    if delete_identical and replays.count() >=2:
        latest = replays[0]
        previous = replays[1]
        
        if (         #all prop/fields are identical 
             latest.status_before == previous.status_before and
             latest.status_after == previous.status_after and
             latest.body_changed == previous.body_changed
        ):
            latest.delete()

from django.utils import timezone
from datetime import timedelta
#fxn for removing replayed req of older days 
def purge_expired_replays():
    #deleting replaylogs older then configured time[days]
    #meant to run as a maintainance task (cron/management command
    ttl_days = get_bb_setting("REPLAY_TTL_DAYS" , None)

    if not ttl_days:
        return #feature disabled
    
    cutoff = timezone.now() - timedelta(days=ttl_days)

    old_logs = ReplayLog.objects.filter(replayed_at__lt=cutoff)

    deleted_count, _ = old_logs.delete() 

    return deleted_count        #
