"""
Jupyter Notification Extension
Custom Jupyter %magic for monitoring long-running cells with notifications.

note: 
This extension was created by Fin Headley to work on his personal computer.
The following assumptions have been made:
    The Jupyter Notebook is being run locally on a MAC OS device
    The user has an iphone that can recieve iMessages

It is setup to work assuming that the computer is an apple device and 
the user is has an Iphone that can recieve iMessages.

How to use:
- Save this file LOCALLY as 'magic_notifications.py' (to the same folder as the Jupyter notebook)
- Input the Iphone number you would like the %magic to notify via iMessage
- In Jupyter notebook, run following in a cell: 
    %load_ext magic_notifications
- In the cell you want notifiactions for, 
    - Use the command %notify_me to get a popup and imessage notification when cell finishes running
"""

import time
from IPython.core.magic import Magics, magics_class, cell_magic
from pync import Notifier
import subprocess

def send_notification(message = "default message"):
    """
    Send a notification to the user's phone via iMessage and computer via notification 

    Parameters
    -----------
    message : str
        the text that will be sent out as an imessage and a popup

    Returns
    --------
    None
        (the message is sent to the devices)
    """
    phone_number = "0000000000"     #Phone number is hard coded in as a string (phone_number = "0000000000")
                                    #You must replace the phone number with a target phone number
                                    #As I run this code locally, from my laptop to my phone I hardcoded my own phone number
                                    #I have removed my number before uploading this to github

    if phone_number == "0000000000":
        raise Exception("Must input a number to send a message")
    
    #this is is osascript that describes the process of sending the message to a target device
    applescript = f'''  
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript], check=True)    #runs the osascript to send the iMessage
    Notifier.notify(message, title='Cell Complete')                 #sends a popup notification to the computer (MacOS)
    
    return



@magics_class
class CellMonitor(Magics):
    """
    Custom Jupyter %magic for monitoring long-running cells with notifications.
    """
    
    def __init__(self, shell):
        super().__init__(shell)

    @cell_magic
    def notify_me(self, line, cell):
        """
        Monitor a specific cell execution.
        
        Parameters
        -----------
        inherited from CellMonitor Class

        Returns
        --------
        None
            The generated message is sent to the devices via send_notification()
        """
        start_time = time.time()    # Used to calculate how long a cell took to ran
        
        # Execute the cell
        result = self.shell.run_cell(cell) # type: ignore #

        end_time = time.time()                                      # Used to calculate how long a cell took to ran
        duration = (end_time - start_time)                          # Duration is the time the cell took to run (or fail) in seconds (float)
        duration_time = time.gmtime(duration)                       # Take the number of seconds and convert it to a struct_time
        duration_text = time.strftime("%H:%M:%S", duration_time)    # Create a HH:MM:SS string for the notification using the struct_time

        #The cell completed running and a notification should be sent out
        if result.success:
            send_notification(                                      #sent as popup and imessage
                f"Jupyter Cell finished after {duration_text}")     #successful completion message
            return
        
        #User interupted cell and stopped it from running
        elif KeyboardInterrupt:
            return #does not send notification as the User would be at their computer and there is no need to notify them
        
        #There was an error encountered and the cell stopped running
        else:
            send_notification(                                      #sent as popup and imessage
                f"ALERT: \n Jupyter Cell failed after {duration_text}")     #Failed cell message 
            return

# Extension loading functions
def load_ipython_extension(ipython):
    """Load the extension"""
    ipython.magics_manager.register(CellMonitor)
    print("Jupyter Notification Extension loaded!")
    print("Commands:")
    print("%%notify_me      - get a notification when a cell completes")
