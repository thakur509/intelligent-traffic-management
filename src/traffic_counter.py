from pathlib import Path
import cv2
import csv
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_PATH = BASE_DIR / "input.mp4"
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "logs.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)

LINE_POSITION = 550
MIN_WIDTH = 80
MIN_HEIGHT = 80
OFFSET = 6
COUNT = 0

cap = cv2.VideoCapture(str(VIDEO_PATH))
if not cap.isOpened():
    raise FileNotFoundError(f"Cannot open video: {VIDEO_PATH}")

bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=100, detectShadows=True
)

with open(CSV_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "count"])

def center_handle(x, y, w, h):
    return int(x + w / 2), int(y + h / 2)

def log_count(count):
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), count])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 5)
    fgmask = bg_subtractor.apply(blur)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(closing, cv2.MORPH_DILATE, kernel)
    _, thresh = cv2.threshold(closing, 200, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (25, LINE_POSITION), (1200, LINE_POSITION), (255, 0, 0), 2)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w >= MIN_WIDTH and h >= MIN_HEIGHT:
            cx, cy = center_handle(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

            if abs(cy - LINE_POSITION) <= OFFSET:
                COUNT += 1
                log_count(COUNT)

    traffic_level = "Low"
    if COUNT > 5:
        traffic_level = "Medium"
    if COUNT > 10:
        traffic_level = "High"

    cv2.putText(frame, f"Count: {COUNT}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Traffic: {traffic_level}", (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Traffic Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()