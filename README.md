# AI-Painter
AI-Painter/Virtual-Painter is a Python [ Computer-Vision / Augmented-Reality(AR) / Automation ] aplication built using the OpenCV library and MediaPipe. This app allows users to paint on the screen in real-time using hand gestures, providing an interactive and intuitive painting experience.

## Features
- Real-time hand detection and tracking.
- Dynamic color selection and eraser functionality.
- Save the paintings with a single gesture.
- User-friendly interface with an intuitive Taskbar for color selection and other options.

## Requirements
- Python 3.x
- OpenCV
- NumPy
- MediaPipe
  
## Installation
1. Install the required packages using the following command:
  ```bash
  pip install opencv-python numpy mediapipe
  ```
2. Ensure that the Taskbar folder contains the necessary images for color selection and other options.

## Usage
1. Run the virtualPainter.py script:
  ```bash
  python virtualPainter.py
  ```
2. Adjust the camera settings and hand placement to start painting.
3. Use your index finger to draw on the screen. Single-finger drawing mode is activated when only the index finger is up.
4. Use two fingers to activate selection mode. Navigate through the Taskbar options by moving your hand over the corresponding regions.
5. Save your artwork by placing two fingers on the designated download region.

## Taskbar Options
The Taskbar provides the following options:

- `Blue:` Select blue color.
- `Red:` Select red color.
- `Yellow:` Select yellow color.
- `Green:` Select green color.
- `White:` Select white color.
- `Eraser:` Activate eraser mode.
- `Download:` Save the current painting.

## File Structure
- `virtualPainter.py`: Main script for the AI-Painter application.
- `fingers.py`: Module for hand detection and tracking.
- Taskbar: Folder containing images for the Taskbar options.
  
## Customization
Feel free to customize the application by adding or modifying Taskbar options, changing color codes, or adjusting brush thickness according to your preferences.

## Acknowledgments
This application utilizes the OpenCV and MediaPipe libraries. Special thanks to their respective communities for providing powerful tools for computer vision and hand tracking.
