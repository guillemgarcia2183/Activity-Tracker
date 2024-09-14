# Add libraries
import cv2
import numpy as np
import pyautogui
import time
import os
import win32gui
import win32con

# Display screen resolution
SCREEN_SIZE = (1920, 1080) #PC resolution size
FPS = 10.0

def create_video_object():
    # Ensure the 'recordings' directory exists
    if not os.path.exists('recordings'):
        os.makedirs('recordings')

    # Define codec
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Create video write object. The recorded file will be in recordings/time.mp4, 
    output = cv2.VideoWriter("recordings/" + time.strftime("%H-%M-%S %d-%m-%y") + ".mp4",
                            fourcc, 10, (SCREEN_SIZE)) 
    
    # Start recording
    starting_recording(output)

    # When we finished, clean all windows
    clean(output)
    
def starting_recording(output):
    print("Starting recording.....")
    print("Press q if you want to stop recording")
    minimized = False
    while True:
        # Make screenshot
        img = pyautogui.screenshot()
        # Convert image into a numpy array. Needed to work with cv2
        frame = np.array(img)
        # Convert BGR colors into RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Show frame
        cv2.imshow("Screen recorder", frame)
        if not minimized:
            minimized = True
            minimize_Window()
        # Write frame to video
        output.write(frame)
        # Condition to quit recording
        if cv2.waitKey(1) == ord("q"): 
            print("Recording finalized!")
            break

def minimize_Window():
    window = win32gui.FindWindow(None, "Screen recorder")
    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

def clean(output):
    # Make sure if everything is closed
    output.release()
    cv2.destroyAllWindows() 

if __name__ == "__main__":
    create_video_object()