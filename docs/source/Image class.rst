Image class
===========

**cvbot.images.Image**

Class functions
---------------

.. py:function:: image.show(pos=None)

   Shows the image on a separate window

   :param pos: Optional "pos" position of displayed window is tuple of x and y coordinates.
   :type pos: tuple(int, int) or None

   
   Examples:

       - Showing an image of a screen region

.. code-block:: python
   from cvbot.capture import get_reigon

   img = get_region((100, 100, 300, 300))
   img.show()

