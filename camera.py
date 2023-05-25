import cv2
# this is for accessing the camera provided that the camera is connected 

def camera_interface():
    #here we are creating an object for the video capture

    cap = cv2.VideoCapture(0)  # 0 for default camera, or specify the camera index if multiple cameras are available

    #this loop is to read the frames from the camera one by one and then showing it on the window named camera that will pop up that we have created in the line 13
    while True:
        ret, frame = cap.read()  # Read a frame from the camera and returns two values one being a boolian value depending on wether the frames were caught or not and the second one being the image represented as an NUMpy array -> this is what makes us able to store a large multidimetion array while performing functions on it.

        cv2.imshow('Camera', frame)  # Display the frame in a window named 'Camera'

        if cv2.waitKey(1) == 27:  # Break the loop if the 'Esc' key is pressed 27 is the ASCII value for the "Esc" key.
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all windows

camera_interface()  # Call the function to start the camera interface