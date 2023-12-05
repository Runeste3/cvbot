import cv2
import numpy as np
import onnxruntime as ort
#from time import time


classifiers = {}
session = None
classes = None

def _init_model(path, clss):
    global session, classes
    session = ort.InferenceSession(path, 
                                   providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    classes = clss


def init_model(path, clss):
    _init_model(path, clss)

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)
#
def detect(img, thresh):
    global session, classes

    if session is None:
        print("Please initiate model using 'init_model' before calling detection function!")
        return ()

    outname = [i.name for i in session.get_outputs()]
    inname = [i.name for i in session.get_inputs()]

    img = img.img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = img.copy()
    image, ratio, dwdh = letterbox(image, auto=False)
    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)

    im = image.astype(np.float32)
    im /= 255
    im.shape

    inp = {inname[0]:im}
    #st = time()
    outputs = session.run(outname, inp)[0]
    #et = time()
    #print("Time ->", round(et - st, 3))

    noutputs = []

    if len(outputs):
        for output in outputs:
            id, x0, y0, x1, y1, _, scr = output
            if scr < thresh:
                continue
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()

            name = classes[int(id)]

            toadd = (box, scr, name)

            noutputs.append(toadd)

    return noutputs 
