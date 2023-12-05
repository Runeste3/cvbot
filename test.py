import images
import cvbot.windows

if __name__ == "__main__":
    img = images.capture_window("~Dransik")
    #img.show()
    #win = windows.get_last_win()
    #win.resize(1080, 720)
    img.sift_feats()