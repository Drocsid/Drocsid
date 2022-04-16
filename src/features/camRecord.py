import cv2


def camrecord():
    record_seconds=int(input("Please enter seconds to record: "))
    frames_per_second = 12.0
    vid_capture = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not vid_capture.isOpened():
        raise IOError("Cannot open webcam")

    # Create a file “.avi” and write in this file.
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter("videos_output.avi", vid_cod, 20.0, (640,480))

    for i in range(int(record_seconds * frames_per_second)):
        ret,frame = vid_capture.read()
        output.write(frame)
        if cv2.waitKey(1) &0XFF == ord('q'):
            break
    # Close the already opened camera
    vid_capture.release()
    # Close the already opened file
    output.release()
    # Close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

camrecord()    
