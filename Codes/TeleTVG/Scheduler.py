#Copyright (c) 2020, KarjaKAK
#All rights reserved.

from datetime import datetime as dt
import asyncio

class Settimer:
    """
    Setting time for scheduling job
    """
    def __init__(self, days = 0, hours = 0, minutes = 0, seconds = 1):
        if days:
            self.days = days * 86400
        else:
            self.days = days
        if hours:
            self.hours = hours * 3600
        else:
            self.hours = hours
        if minutes:
            self.minutes = minutes * 60
        else:
            self.minutes = minutes
        self.seconds = seconds
        self.settime = None
        
    def settimer(self):
        # Settimer in seconds.
        
        self.settime = sum([self.days, self.hours, self.minutes, self.seconds])
        return self.settime
    
    def scheduletime(self):
        # Setting future date.
        
        tdy = int(dt.timestamp(dt.now().replace(microsecond = 0)))
        if self.settime:
            return tdy + self.settime
        else:
            return tdy + self.settimer()
    
    def scheduletk(self):
        # Setting timer in microseconds.
        
        if self.settime:
            return self.settime * 1000
        else:
            return self.settimer() * 1000
    
class Scheduler(Settimer):
    """
    Scheduler job for running a function.
    Using asyncio.
    """
    
    async def schedule(self, func, *args):
        # Set to sleep.
        
        await asyncio.sleep(self.settimer())
        func(*args)
        
    async def runschedule(self, func, *args):
        # Schedule runner.
        
        rt = list(*args)
        task = {}
        for i in range(len(rt)):
            task[i] = asyncio.create_task(self.schedule(func, rt[i]))
        for i in task:
            await task[i]
        
    def runmain(self, func, *args):
        # Calling asyncio.
        
        asyncio.run(self.runschedule(func, *args))
        

if __name__ == '__main__':
    import time
    def test(num):
        print(num**2)
    tm = time.perf_counter()
    a = Scheduler(seconds=1)
    a.runmain(test, (100**2, 
                     1000**2, 
                     10000**2, 
                     100000**2, 
                     1000000**2, 
                     100000000**2, 
                     1000000000**2, 
                     1000000000**2, 
                     1000000000**2, 
                     100000000**2, 
                     100000000**2, 
                     100000000**2, 
                     10000000**2, 
                     10000000**2))
    print(f'{int(time.perf_counter()-tm)} seconds')
    print('Woow')