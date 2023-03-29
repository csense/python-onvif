import cv2
import time
import os
from datetime import datetime, timedelta

# Open the video stream
cap = cv2.VideoCapture('rtsp://admin:admin@192.168.1.4:8554/Streaming/Channels/101')

# Define the duration (in seconds) of each video segment
segment_duration = 60  # 1 minutes

# Define the current segment start time
segment_start_time = time.time()

# Create the video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

today = datetime.now().strftime('%Y-%m-%d')
if not os.path.exists(today):
    os.mkdir(today)

print('Stream activated, listening...')
# Loop through frames and save them to disk
while (cap.isOpened()):
    ret, frame = cap.read()
    if out is None:
        # Generate a unique filename for the output video
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        output_file_name = f'{today}/video_stream_{timestamp}.mp4'
        # Create the video writer object when the first frame is available
        out = cv2.VideoWriter(output_file_name, fourcc, 15.0, (frame.shape[1], frame.shape[0]))
    # Write the frame to the output video
    out.write(frame)
    # Check if the current segment has reached its duration
    elapsed_time = time.time() - segment_start_time
    if elapsed_time >= segment_duration:
        # Release the output video writer
        out.release()
        out = None
        # Reset the segment start time
        segment_start_time = time.time()
        print(f"Video saved at: {output_file_name}")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.01)

# Release the resources
cap.release()
cv2.destroyAllWindows()
