import cv2
import numpy as np
import pyautogui
import time
import os
import win32gui
import win32con
import matplotlib.pyplot as plt
from keras.models import load_model
import matplotlib.patches as mpatches
import tkinter as tk
from threading import Thread
import atexit
import queue

# Display screen resolution
SCREEN_SIZE = (1920, 1080)  # PC resolution size
FPS = 20.0



class RecorderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Recorder")
        self.save_file = False
        self.recording = False
        self.plot_queue = queue.Queue()

        self.save_button = tk.Button(master, text="Save Recording: Disabled", command=self.toggle_save)
        self.save_button.pack()

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording, state=tk.NORMAL)
        self.start_button.pack()

        self.quit_button = tk.Button(master, text="Stop Recording", command=self.quit_recording)
        self.quit_button.pack()

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.recording = True
        self.recording_thread = Thread(target=self.create_video_object, args=(self.save_file,))
        self.recording_thread.daemon = True  # Set the thread as a daemon
        self.recording_thread.start()

    def quit_recording(self):
        self.recording = False
        self.master.mainloop()
        os._exit(0)
        
    def toggle_save(self):
        self.save_file = not self.save_file
        if self.save_file:
            self.save_button.config(text="Save Recording: Enabled")
        else:
            self.save_button.config(text="Save Recording: Disabled")

    def create_video_object(self, save_file):
        model = load_model('multiclass_model.h5')
        class_counts = [0] * model.output_shape[1]  # Initialize counts for each class
        minimized = False
        initial_time = time.time()
        output = None
        if save_file:
            if not os.path.exists('recordings'):
                os.makedirs('recordings')

            # Define codec
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            # Create video write object. The recorded file will be in recordings/time.mp4,
            output = cv2.VideoWriter("recordings/" + time.strftime("%H-%M-%S %d-%m-%y") + ".mp4",
                                    fourcc, 5, (SCREEN_SIZE))

        while self.recording:
            # Make screenshot
            img = pyautogui.screenshot()
            # Convert image into a numpy array. Needed to work with cv2
            frame = np.array(img)
            # Convert BGR colors into RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if not minimized:
                minimized = True
                self.minimize_Window()

            # Write frame to video
            if save_file:
                output.write(frame)

            # Preprocess the frame
            frame = cv2.resize(frame, (224, 224))  # Resize to 224x224
            frame = frame / 255.0  # Normalize pixel values

            # Add a new axis to represent the width dimension
            frame = frame[np.newaxis, ...]

            # Make a prediction with the model
            prediction = model.predict(frame)

            # Increment the count for the predicted class
            predicted_class = np.argmax(prediction)
            class_counts[predicted_class] += 1

            # Wait to next frame
            time.sleep(1)

        time_elapsed = time.time() - initial_time
        self.plot_queue.put((class_counts, time_elapsed))
        self.show_plot(class_counts, time_elapsed)
        self.show_pie_plot(class_counts, time_elapsed)
        self.clean(save_file, output)

    def minimize_Window(self):
        window = win32gui.FindWindow(None, "Screen recorder")
        win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

    def clean(self, save_file, output):
        # Make sure if everything is closed
        if save_file:
            output.release()
        cv2.destroyAllWindows()

    def show_plot(self, class_counts, time_elapsed):
        # Calculate the percentages for each class
        distribution = [(count) / 60 for count in class_counts]

        # Create the bar plot
        labels = ["ChatGPT", "Campus Virtual", "Github", "Gmail", "Outlook", "Phind", "Spotify", "Twitch", "Twitter", "Visual Studio", "Youtube"]
        colors = ["blue", "red", "red", "red", "red", "blue", "green", "green", "green", "red", "green"]

        # Sort the labels and values in descending order of percentages
        sorted_labels, sorted_values, sorted_colors  = zip(*sorted(zip(labels, distribution, colors), key=lambda x: x[1], reverse=False))

        # Create the horizontal bar plot
        bars = plt.barh(sorted_labels, sorted_values, color=sorted_colors)
        plt.xlabel('Minutes used')
        plt.ylabel('Class')
        plt.suptitle(f'Class Distribution')
        plt.title(f'Time elapsed: {round(time_elapsed/60, 2)} minutes')

        # Create a custom legend
        blue_patch = mpatches.Patch(color='blue', label='Artificial Inteligence')
        red_patch = mpatches.Patch(color='red', label='Working material')
        green_patch = mpatches.Patch(color='green', label='Entertainment')

        plt.legend(handles=[blue_patch, red_patch, green_patch], loc='lower right')

        plt.show()

    def show_pie_plot(self, class_counts, time_elapsed):
        # Calculate the percentages for each class
        total_counts = sum(class_counts)
        percentages = [(count / total_counts) * 100 for count in class_counts]

        # Create the labels and colors
        labels = ["ChatGPT", "Campus Virtual", "Github", "Gmail", "Outlook", "Phind", "Spotify", "Twitch", "Twitter", "Visual Studio", "Youtube"]
        colors = ["blue", "red", "red", "red", "red", "blue", "green", "green", "green", "red", "green"]

        # Calculate the sum of percentages for each color
        color_percentages = {}
        for label, percentage, color in zip(labels, percentages, colors):
            if color not in color_percentages:
                color_percentages[color] = 0
            color_percentages[color] += percentage

        # Create custom labels for the pie chart
        custom_labels = {
            "blue": "Artificial Intelligence",
            "red": "Working Material",
            "green": "Entertainment"
        }

        # Create the pie chart
        pie_labels = [custom_labels[color] for color in color_percentages.keys()]
        pie_values = list(color_percentages.values())
        plt.pie(pie_values, labels=pie_labels, autopct='%1.1f%%')
        plt.title(f'Type of activity distribution')
        plt.show()

root = tk.Tk()
my_gui = RecorderGUI(root)
root.mainloop()