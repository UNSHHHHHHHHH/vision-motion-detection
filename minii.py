import cv2
import time
  # Optional for sound alarm
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Function to send email alert (optional)
def send_email_alert():
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = "your_email_password"
    subject = "Security Alert: Motion Detected!"
    body = "Motion has been detected at your house."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Initialize the webcam for video capturing
cap = cv2.VideoCapture(0)

# Define variables for motion detection
first_frame = None
motion_detected = False
motion_time = None

# Define minimum area of motion to detect
min_motion_area = 5000  # Adjust this as needed for sensitivity

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    text = "No Motion"

    # Resize the frame and convert it to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Initialize the first frame for motion detection
    if first_frame is None:
        first_frame = gray
        continue

    # Calculate the difference between the first frame and current frame
    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours (motion areas)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check contours for significant motion
    for contour in contours:
        if cv2.contourArea(contour) < min_motion_area:
            continue
        # If motion detected
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        text = "Motion Detected"
        motion_detected = True
        motion_time = datetime.now()

    # Display status on the video feed
    cv2.putText(frame, "Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Show the video feed
    cv2.imshow("House Security", frame)

    # Trigger an alert when motion is detected
    if motion_detected:
        print(f"Motion detected at {motion_time}")
        playsound('alarm.wav')  # Play an alarm sound (optional)
        send_email_alert()  # Send an email alert (optional)
        motion_detected = False  # Reset motion detection

    # Break the loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

