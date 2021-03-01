import cv2
import numpy as np

# Load Yolo

net = cv2.dnn.readNet("MansXarxa/models/yolov3.weights", "MansXarxa/models/yolov3.cfg")
classes = []
with open("MansXarxa/models/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


def trobarpersona(img):
    # Loading image
    # img = cv2.imread("Maadalt.jpg")
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            x1 = x - 10
            y1 = y - 20
            x2 = x + w
            y2 = y + h

            # label = str(classes[class_ids[i]])
            color = (222,0,223)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            # cv2.putText(img, label, (x1, y + 30), font, 3, color, 3)

            crop_img = img[y1:y2, x1:x2]
            # cv2.imshow("xuet", crop_img)
            return crop_img, x1, y1

    # cv2.imshow("Image", img)
