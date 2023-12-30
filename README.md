# CVBot for desktop automation

**CVBot** is a python package developed to make using computer vision techniques easier and simple to use. 
Its main focus is to *aid in automating visual desktop related tasks* for repetitive work, games and others. Working "like a human".

-------------------------------------------------------------------------------
## Features

- [x] Mouse & keyboard control.
- [x] Control windows and get their position.
- [x] OpenCV image wrapper `Image class` to easily crop, resize, show, and convert images.
- [x] Flexible digits & numbers recognition/matching.
- [x] Powerful image search on screen or a local file.
- [x] Implements sophisticated image search techniques like SIFT.
- [x] Color based object detection.
- [x] Very fast screenshot grab.
- [x] Accurate OCR integrated with `Image class`.
- [x] Artificial Intelligence based object detection support using Yolov7.

## Upcoming

- [ ] Better documentation.
- [ ] More QOL functions and classes.
- [ ] More detection options.

-------------------------------------------------------------------------------
## Simple example

**Detect an object on the screen**

```python
    from cvbot.capture import screenshot
    from cvbot.io import read_img
    from cvbot.match import look_for


    obj = read_img("object.png")    # Read 'object.png' file, (an object currently visible on screen)
    scimg = screenshot()            # Take a screenshot

    pos = look_for(obj, scimg, 0.6) # Image search function, parameters: (needle, haystack, search confidence 1 = 100%)
    print(pos)                      # PRINTS: (188, 538) # None if not found
```

-------------------------------------------------------------------------------
## Links

[Full Documentation](https://cvbot.rtfd.io/)
[Github](https://github.com/Runeste3/cvbot)
