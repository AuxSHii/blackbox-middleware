from django.utils import timezone
from datetime import timedelta

#fxn for retunring req]faulures occured in last x min
def last_minutes(queryset , minutes):
    """return record created in last x min [filter by timestamp]"""
    cutoff_time = timezone.now() - timedelta(minutes=minutes)   # cutoff_time = convt x minute into the value of time of lsat x mnute in the  format of timezone of our models's timestamp 
    return queryset.filter(timestamp__gte=cutoff_time)   # filter req by time greater then cutoff time
    

