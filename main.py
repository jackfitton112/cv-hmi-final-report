import cv2
from ultralytics import YOLO

# Load Haar cascades for mouth detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('mouth.xml')  # Replace with the path to the mouth cascade

# Load the YOLOv8 model for object detection
model = YOLO('yolov8n.pt')  # Replace 'yolov8n.pt' with a custom-trained model if needed

# Set up webcam capture
cap = cv2.VideoCapture(4)

while True:
    # Capture frame from the webcam
    ret, image = cap.read()
    if not ret:
        break

    # Convert to grayscale for mouth detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Define ROI for the mouth (lower half of the face)
        roi_gray = gray[y + int(h / 2):y + h, x:x + w]
        roi_color = image[y + int(h / 2):y + h, x:x + w]

        # Detect mouth within the ROI
        mouths = mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=11)

        for (mx, my, mw, mh) in mouths:
            # Draw rectangle around the mouth
            cv2.rectangle(roi_color, (mx, my), (mx + mw, my + mh), (255, 0, 0), 2)
            cv2.putText(roi_color, "Mouth", (mx, my - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Perform object detection using YOLO
    results = model(image)

    for result in results[0].boxes.data:
        x1, y1, x2, y2, confidence, class_id = result.tolist()
        class_name = model.names[int(class_id)]

        # Print detected item and its location
        print(f"Detected: {class_name} at {(x1, y1, x2, y2)} with confidence {confidence:.2f}")

        # Draw bounding boxes and labels on the image
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, f"{class_name} {confidence:.2f}", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Mouth and Object Detection', image)

    # If the key 'q' is pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
