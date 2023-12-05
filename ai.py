from easyocr import Reader

reader = None

def init_ocr(langs, model_path=None):
    """
    list(str) -> None
    Initiate easyocr NN model for future detection
    """
    global reader

    if reader is None:
        reader = Reader(langs, gpu=True, verbose=False, 
                        model_storage_directory=model_path)
    else:
        print("\nOCR model is already initiated!")

def read(img, allowlist=None):
    """
    Image, str | None -> str
    Use easyocr to read string in given image
    and return it
    """
    global reader

    if reader is None:
        print("\nOCR model was not initiated, please call 'init_ocr' before calling 'read' function")
    else:
        return "".join(reader.readtext(img.img, detail=0, allowlist=allowlist))
