import os
import cv2

# Set the input directory containing your .mp4 files
input_dir = 'recordings'

# Set the output directory for extracted images
output_dir = 'training_samples'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create subfolders for each class
classes = []  # list to store unique class labels
for filename in os.listdir(input_dir):
    if filename.endswith(".mp4"):
        # Extract the class label from the filename
        label = filename.split('_')[0]  # assuming the class label is before the first underscore
        if label not in classes:
            classes.append(label)
            class_dir = os.path.join(output_dir, label)
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)

# Iterate through all .mp4 files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".mp4"):
        # Extract the class label from the filename
        label = filename.split('_')[0]  # assuming the class label is before the first underscore

        # Create a video capture object
        cap = cv2.VideoCapture(os.path.join(input_dir, filename))

        # Extract frames from the video
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            # Save the frame as an image
            img_filename = f"{filename[:-4]}_{frame_count:03d}.jpg"
            img_path = os.path.join(output_dir, label, img_filename)
            cv2.imwrite(img_path, frame)

        # Release the video capture object
        cap.release()