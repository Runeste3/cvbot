CVBot for desktop automation
============================

**CVBot** is a python package developed to make using computer vision techniques easier and simple to use.
    Its main focus is to aid in automating visual desktop related tasks for repetitive work, games and others. Working "like a human".


Features
--------

- Mouse & keyboard control.
- Control windows and get their position.
- OpenCV image wrapper(``Image class``) to easily crop, resize, show, and convert images.
- Flexible digits & numbers recognition/matching.
- Powerful image search on screen or a local file.
- Implements sophisticated image search techniques like SIFT.
- Color based object detection.
- Very fast screenshot grab.
- Accurate OCR integrated with ``Image class``.
- Artificial Intelligence based object detection support using Yolov7.


Simple example
--------------

.. code-block:: python
   :caption: Detect an object on the screen

    from cvbot.capture import screenshot
    from cvbot.io import read_img
    from cvbot.match import look_for


    obj = read_img("object.png")    # Read 'object.png' file, (an object currently visible on screen)
    scimg = screenshot()            # Take a screenshot

    pos = look_for(obj, scimg, 0.6) # Image search function, parameters: (needle, haystack, search confidence 1 = 100%)
    print(pos)                      # PRINTS: (188, 538) # None if not found



Links
------

Full Documentation: 
.. _a link: https://cvbot.rtfd.io/

Github: 
.. _a link: https://github.com/Runeste3/cvbot 
