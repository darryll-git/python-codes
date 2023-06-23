import cv2
import numpy as np
from openpose import OpenPose

class SkillDetector:
    def __init__(self, skill):
        self.skill = skill
        self.net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.openpose = OpenPose()
        
    def detect_skill(self, image):
        # Perform object detection using YOLOv3
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Process the object detection results
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5 and class_id == 0:  # Class ID 0 represents person
                    center_x = int(detection[0] * image.shape[1])
                    center_y = int(detection[1] * image.shape[0])
                    width = int(detection[2] * image.shape[1])
                    height = int(detection[3] * image.shape[0])
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform pose estimation using OpenPose
        keypoints = []
        for box in boxes:
            left, top, width, height = box
            roi = image[top:top+height, left:left+width]
            keypoints.append(self.openpose.detect_pose(roi))

        # Determine if the specified skill is being performed based on keypoints
        is_skill = self.check_skill(keypoints)  # Custom function to determine the specific skill based on keypoints

        return is_skill

    def check_skill(self, keypoints):
        # Custom logic to determine if the specified skill is being performed
        # Modify or add specific rules based on the keypoints for the skill

        # Example logic for push-ups: Check if keypoints for wrists are below a certain threshold height
        wrist_height_threshold = 0.8  # Adjust this threshold based on your requirements

        left_wrist = keypoints[0][7]  # Keypoint index for left wrist
        right_wrist = keypoints[0][4]  # Keypoint index for right wrist

        is_pushup = (
            left_wrist[1] > wrist_height_threshold and
            right_wrist[1] > wrist_height_threshold
        )

        # Example logic for pull-ups: Check if keypoints for elbows are above a certain threshold height
        elbow_height_threshold = 0.2  # Adjust this threshold based on your requirements

        left_elbow = keypoints[0][6]  # Keypoint index for left elbow
        right_elbow = keypoints[0][3]  # Keypoint index for right elbow

        is_pullup = (
            left_elbow[1] < elbow_height_threshold and
            right_elbow[1] < elbow_height_threshold
        )

        # Return the result based on the specified skill
        if self.skill == 'pushup':
            return is_pushup
        elif self.skill == 'pullup':
            return is_pullup
        else:
            return False

# Create a Pushup Detector
pushup_detector = SkillDetector(skill='pushup')

# Load the input image
image = cv2.imread("image.jpg")

# Detect the skill (push-up or pull-up)
is_pushup = pushup_detector.detect_skill(image)

# Display the result
label = "PUSHUP" if is_pushup else "NOT A PUSHUP"
cv2.putText(image, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with the result
cv2.imshow("Skill Detector", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
