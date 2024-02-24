import cv2
import numpy as np

class BlockDetector:
    def __init__(self, color_range):
        self.cap = cv2.VideoCapture(0)  # Initialize the camera
        self.color_range = color_range  # Color range for detection in LAB space

    def preprocess_frame(self, frame):
        """Resize, apply Gaussian Blur, and convert to LAB color space."""
        resized_frame = cv2.resize(frame, (640, 480))
        blurred_frame = cv2.GaussianBlur(resized_frame, (5, 5), 0)
        lab_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2LAB)
        return lab_frame

    def detect_block(self, frame):
        """Detect block by color and return its contour and mask."""
        mask = cv2.inRange(frame, self.color_range[0], self.color_range[1])
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            return max_contour, mask
        return None, mask

    def label_block(self, frame, contour):
        """Draw contour and center on the frame."""
        if contour is not None:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                cv2.putText(frame, "Block", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    def run(self):
        """Main method to run the block detection."""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            processed_frame = self.preprocess_frame(frame)
            contour, _ = self.detect_block(processed_frame)
            self.label_block(frame, contour)
            cv2.imshow('Block Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
        self.cap.release()
        cv2.destroyAllWindows()
