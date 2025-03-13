import datetime
import threading
import time




class Reminder:

    def __init__(self):
        self.dates = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday"
        }       

        self._day = None
        self._weekday = None
        self._comment = None

        self._status = False
        self._statusComment = -1

        


        # Dont forget to rmeove daemon
        print('reminders.py     Initializing background process')
        backgroundThread = threading.Thread(name='background', target=self.checkReminder, daemon=True)
        backgroundThread.start()
        print('reminders.py     Finished!')

    def setWeekday(self, weekday, comment):
        weekday = weekday.lower()
        if weekday not in self.dates.values():
            raise ValueError(f"\n\nInvalid weekday: {weekday}")
        
        self._weekday = weekday.lower()
        self._comment = comment

    def checkReminder(self):
        while True:
            if self._weekday:  # Check if weekday check is set
                todays_day_number = datetime.datetime.today().weekday()
                if self.dates[todays_day_number] == self._weekday: # If reminder is today
                    #print(f"reminders.py    Reminder: {self._comment}")
                    self._status = True
                    self._statusComment = self._comment
                else:
                    self._status = False
                    self._statusComment = -1
            time.sleep(10)  # Prevent CPU overuse

    def getStatus(self):
        '''
        Returns
        -------
        _status
            1 if reminder is today, 0 if not.
        
        _statusComment
            The reminder comment, -1 if not today
        """
        '''
        return [self._status, self._statusComment]
