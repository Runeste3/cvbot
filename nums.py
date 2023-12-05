from cvbot.io import read_img
from cvbot.colors import threshold, count_clr
from cvbot.images import Image
from cvbot.match import mse


FILES = [] 
TCLR = None

def init_reader(pth, clr, slant=True):
    """
    str, Color | None, bool -> None
    Initiate reader by loading number images
    from given path 'pth'
    Color of the number to read,
    if 'clr' is None use automatic color detection
    'slant' is True if digit reading includes a slant
                between the numbers
    """
    global FILES, TCLR

    if FILES == []:
        for i in range(10):
            FILES.append(read_img("{}{}.png".format(pth, i), "grey"))

        if slant:
            FILES.append(read_img("{}slant.png".format(pth), "grey"))

        TCLR = clr

def trim(bim):
    """
    Binary Image -> Binary Image
    Remove all the black columns in the given
    binary iamge 
    """
    w, _ = bim.size
    fin = 0
    tin = w

    fwts = False
    for x in range(0, w):
        clim = Image(bim.img[:, x])
        wts = count_clr(clim, 255)
        if wts == 0:
            fwts = True 
            continue
        elif fwts:
            fin = x

        break

    fwts = False
    if w >= 2:
        for x in range(w - 1, 0, -1):
            clim = Image(bim.img[:, x])
            wts = count_clr(clim, 255)
            if wts == 0:
                fwts = True
                continue
            elif fwts:
                tin = x + 1
            break

        return Image(bim.img[:, fin:tin])
    else:
        return bim
    

def parse(bim):
    """
    Binary Image -> int | None
    Read the digit in given binary image
    """
    global FILES
    data = []
    
    for i in range(10):
        try:
            num = FILES[i]
            cimg = bim.resize(num.size)
        except Exception as e:
            #print(e, num.size, bim.size)
            return None 
        sqdf = mse(cimg, num)
        data.append(sqdf if sqdf != 0 else 0.01)

    #--------Print result and show image-----------
    #for i, d in enumerate(data):
    #    print(i, "{}%".format(int(d * 1000) / 10))
    # 
    #print("--------------------")
    #----------------------------------------------

    res = data.index(min(data))
    return res

def get_dig(bim):
    """
    Binary Image -> Binary Image, Binary Image
    Return the first digit in the given binary image
    of numbers, and return the remaining numbers
    as a new binary image
    """
    w, _ = bim.size
    ind = w

    for x in range(w):
        clim = Image(bim.img[:, x])
        wts = count_clr(clim, 255)
        if wts == 0:
            ind = x
            break

    return Image(bim.img[:, :ind]), None if ind == w else Image(bim.img[:, ind:])

def slntind(dst):
    """
    Binary Image -> int
    Find slant in 'dst' and 
    return its index in 'dst'
    """
    global FILES

    slant = FILES[-1]
    sw, _ = slant.size
    w, _  = dst.size

    rec = []

    for x in range(w):
        if (x + sw) <= w:
            pim = Image(dst.img[:, x:x+sw])
            sdf = mse(pim, slant)
            rec.append(sdf)

    return rec.index(min(rec))


def crptoslant(dst):
    """
    Binary Image -> Binary Image
    Find the slant "/" in given binary image "dst"
    And crop the image upto the slant(not including the slant)
    """
    ind = slntind(dst)

    return Image(dst.img[:, :ind])

def segment(dst, slant):
    """
    Binary Image, bool -> [Binary Image][1+]
    Partition given binary image of numbers
    into image of each digit from left to right
    """
    digs = []

    if slant:
        dst = crptoslant(dst)

    times = 0
    while not (dst is None) and (times < 10):
        dst = trim(dst)
        dig, dst = get_dig(dst)
        digs.append(dig.copy())
        times += 1

    return digs

def nread(img, clr_var=0, cstmclr=None, slant=True):
    """
    Image, int, Color, int | None -> int 
    Read the number shown in given image
    """
    global FILES, TCLR

    if FILES:
        if cstmclr is None:
            clr = TCLR
        else:
            clr = cstmclr

        dst  = threshold(img, clr, clr_var)
        digs = segment(dst, slant)

        nms = [str(parse(d)) for d in digs]

        return int("".join(nms)) if not ("None" in nms) else None
    else:
        print("Please initiate number reader before running 'read' function")
