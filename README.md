# Intelligent Traffic Management System

A simple Python OpenCV project that detects moving vehicles in a traffic video, counts them when they cross a virtual line, and estimates traffic density.

## Features
- Vehicle detection using OpenCV background subtraction
- Vehicle counting with a line-crossing method
- Traffic level display: Low, Medium, High
- CSV logging of vehicle counts with timestamps
- Easy to run on Windows

## Project Structure
```text
traffic-Project/
├── images/
│   ├── terminal_output.png
│   └── traffic_output.png
├── input.mp4
├── src/
│   └── traffic_counter.py
├── data/
│   └── logs.csv
└── output/
```

## Requirements
- Python 3.x
- OpenCV
- NumPy

## Install Dependencies
```bash
pip install opencv-python numpy
```

## How to Run
1. Place your video file in the project root and name it `input.mp4`.
2. Open terminal in the project folder.
3. Run the script:

```bash
python src\traffic_counter.py
```

## Input & Output Screenshots

### Running the Project

> This screenshot shows the successful execution of the traffic counter application from Windows PowerShell.

<p align="center">
  <img src="images/terminal_output.png" alt="Terminal Output" width="900">
</p>

---

### Traffic Detection Output

> This screenshot shows the live vehicle detection, counting, and traffic density estimation using OpenCV.

<p align="center">
  <img src="images/traffic_output.png" alt="Traffic Detection Output" width="900">
</p>

## How It Works
- The video is read frame by frame.
- Moving objects are detected using background subtraction.
- A virtual line is drawn on the frame.
- When a vehicle crosses the line, the count increases.
- The total count is shown on the screen.
- Each count is saved in `data/logs.csv`.

## Controls
- Press `q` to quit the video window.

## Output
- Live video with detected vehicles
- Total vehicle count
- Traffic density label
- CSV log file in the `data` folder

## Future Improvements
- Use YOLO for better vehicle detection
- Add signal timing control
- Add ambulance priority detection
- Add a dashboard with Flask or Tkinter
