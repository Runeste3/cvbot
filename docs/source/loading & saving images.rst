Loading and saving images from disk
===================================

**cvbot.io**

This module is used for input/output of images(loading and saving).

Functions
---------

- save_image(img, pth)

  Given an image and a local path, write that image to the given path.

.. py:function:: save_img(img=Image, pth=str)

        Write given image "img" to the local path "pth"

        :param img: The image to write.
        :param pth: The path to save the image to.
        :type img: Image
        :type tph: str 

- Examples

        Save a screenshot to the folder "images"

.. code-block:: Python
   from cvbot.io import save_img
   from cvbot.capture import screenshot

   img = screenshot()
   save_img(img, "images/screenshot.png")

