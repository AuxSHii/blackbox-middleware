from django.db import models

class RecordedRequest(models.Model):
    # storing a snapshot of HTTP REQUEST + RESPONSE 
    # to replay later

    # requested data table

  method = models.CharField(max_length=10)    # for like GET, POST
  path = models.TextField()                      #api/orders/42   example
  query_string = models.TextField(blank=True)

  headers = models.JSONField()          #these are for request headers
  body_raw = models.TextField(null=True , blank=True) # raw body here which we use in replay fxn as it is the exact body request use int he django;s test client fxn
  body_parsed = models.JSONField(null=True , blank=True) # a json parsed body for inspection 

  # for respnse data

  response_status = models.IntegerField()
  response_body = models.JSONField(null=True, blank=True)

  #debug metadata

  ip_address = models.GenericIPAddressField(null=True , blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)

  #will help filter bugs later (maybe)

  tag = models.CharField(max_length=100 , blank=True)

  def __str__(self):
        return f"{self.method}  {self.path} -> {self.response_status}"


#it should store

#what the user sent - method,headers,body
#where it was sent - path
#what server/our backened replied - response_status , respnse_body
#when the req. occured/sent to server  - timestamp
#optional labeling we can do - tag (ex: "payment_error")   

