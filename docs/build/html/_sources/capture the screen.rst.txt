Capture the screen
==================

**cvbot.capture**

Take an image of the screen, either the whole screen or part of it, functions in this module will return an image of class 'Image'.

Functions
---------

.. py:function:: capture.screenshot(grey=False)

        Return an Image of the whole screen

        :param grey: default 'False' returns grey image of the screen if True
        :type grey: bool

        - Examples:

         Simple example

.. code-block:: python
   
   from cvbot.capture import screenshot

   img = screenshot()

