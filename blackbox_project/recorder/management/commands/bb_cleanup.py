from django.core.management.base import BaseCommand   #for terminal cmds
from recorder.retention import purge_expired_replays  #my fxn for deleting old logs of replayed request used in the cmd

class Command(BaseCommand):      #class of cmds inherting from BaseCmd
    help = "clean old BLACKBOX replay logs based on TILL settings"  #


    def handle(self , *args , **kwargs):  #method runs at cmd args adn kwargs to allow optional cli inputs later on
        deleted = purge_expired_replays()   #calling my deleting log fxn returning into deleted - returnng value possibilities like 0=till is diabled , 5=delted 5 rows

        if deleted is None:      #tunred offf from settings
            self.stdout.write(self.style.WARNING("BLACKBOX TILL disabled"))  
            # safe print in djang(yellow coloured o/p (message))
        else:      #IF NOT NONE OR DISABLED OR 0
            self.stdout.write(   #any other input of days [numeric value]
                self.style.SUCCESS(f"Deleted {deleted} expired replay logs")
                #print in terminal(the sucess green print( msg:to delte n reolay logs)) 
        )
    