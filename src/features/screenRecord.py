import cv2
import numpy as np
import pyautogui


def screenrecord():
    # The time you want to record in seconds
    record_seconds = int(input("Please enter secondes to record: "))
    # Display screen resolution
    SCREEN_SIZE = tuple(pyautogui.size())
    # Define the codec (compresses and decompresses digital video)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frames_per_second = 12.0
    # create the video write object
    out = cv2.VideoWriter("output.avi", fourcc, frames_per_second, (SCREEN_SIZE))
    # Keep capturing screenshots and writing to the file in a loop until the seconds are passed
    for i in range(int(record_seconds * frames_per_second)):
        # Make a screenshot
        img = pyautogui.screenshot()
        # Convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)
        # Convert colors 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        # if the user clicks q, it exits
        if cv2.waitKey(1) == ord("q"):
            break

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()
