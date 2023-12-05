Windows control and management
==============================

**cvbot.windows**

This only works on "Windows" OS.

This module is used to control windows position, size and others.

Window class
------------

**class functions**:

- reposition the window

Change window position top-left corner to (x, y)

.. py:function:: window.repos(x:int, y:int)
   Change position of window to (x, y) coordinates on screen


Examples:
 - Change window position to the top-left corner of the screen

.. code-block:: Python
   from cvbot import windows

   window = windows.get_window("chrome")
   window.repos(0, 0) # Top-left corner


