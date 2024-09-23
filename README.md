# Screen Recorder to identify an user activity 
## Last update: September 2024

## 1. Objectives
1. Implement a screen recorder using Python's cv2 library to capture the user's screen activity.
2. Develop a deep learning (CNN) model to classify and identify which application or website the user is interacting with (e.g., work-related tools, social media, etc.).
3. Combine the screen recorder with the trained model to analyze and detect user activity in real-time and provide visualized results.
4. Develop an API version of the code for easy integration and usage.

## 2. Requirements
### Python Screen Recorder Requirements
To capture the screen, you'll need the following libraries:
```
pip install opencv-python

pip install pyautogui
```

### CNN Model Training Requirements
To train a Convolutional Neural Network (CNN) model, install these dependencies:
```
pip install tensorflow numpy matplotlib scikit-learn
```

## 3. Usage and Results
This section will demonstrate examples of how the screen recorder and CNN model classify user activities during the screen capture.

![Bar chart of identified classes](./images/1.png)

![Pie chart of type of activity](./images/2.png)

## 3. Repositories 
· /Screen-recorder: Contains the Python code to create a screen recorder using the cv2 library.

· /CNNmodel: Code for training the CNN model to classify applications or websites using recorded screen samples.

· /Create_Training: Script to process screen recordings into training data. Takes .mp4 files as input and outputs frame-by-frame folders for CNN training.


## Participants
Guillem Garcia Dausà (guillemgarcia2183)

Contact e-mail: garcia.guillem.dausa@gmail.com

