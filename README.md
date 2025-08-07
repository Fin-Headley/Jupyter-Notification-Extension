# Jupyter-Notification-Extension
Custom Jupyter %magic for notifications on long-running cell completion.

This extension was created by Fin Headley to work with Jupyter Notebook on his personal computer.

It is setup to work assuming that the computer is an apple device and 
the user is has an iphone that can recieve iMessages.


**_How to use:_**

Save this file locally as 'magic_notifications.py' (to the same folder as the Jupyter Notebook that you want to use it with)

Edit the file, replacing phone_number with the number you would like the %notify_me magic to notify via iMessage

In the Jupyter notebook, run following in a cell:
```Python
%load_ext magic_notifications
```
In the cell you want to be notified about:
- Use the command %notify_me to get a popup and imessage notification when cell finishes running
```Python
%notify_me

#any code you want to run in the cell
```
