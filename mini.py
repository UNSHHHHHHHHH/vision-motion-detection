import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

# Set up email alert (Optional)
def send_email_alert(subject, body):
    try:
        # SMTP setup (using Gmail SMTP here)
        sender_email = "your_email@gmail.com"
        receiver_email = "receiver_email@gmail.com"
        password = "your_email_password"
        
        # Compose the email
        message = MIMEText(body)
        message["Subject"] = 
        
        message["From"] = sender_email
        message["To"] = receiver_email

        # Send email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for webcam

# Initialize motion detection
_, frame1 = cap.read()
_, frame2 = cap.read()

# Set up a directory to save captured images
capture_dir = "captured_images"
if not os.path.exists(capture_dir):
    os.makedirs(capture_dir)

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)  # Compare two frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # Apply threshold
    dilated = cv2.dilate(thresh, None, iterations=3)  # Dilate the threshold
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
    
    # Draw rectangles around detected motion
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue  # Ignore small contours
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Capture the image if motion is detected
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{capture_dir}/motion_{timestamp}.jpg"
        cv2.imwrite(filename, frame1)
        
        print(f"Motion detected! Image saved as {filename}")
        
        # Send an alert via email (optional)
        send_email_alert(
            subject="Motion Detected!",
            body=f"Motion detected at {timestamp}. Check the captured image."
        )

    # Display the video feed
    cv2.imshow("House Surveillance", frame1)
    
    # Update frames
    frame1 = frame2
    _, frame2 = cap.read()
    
    # Exit on pressing 'q'
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()