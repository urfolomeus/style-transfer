import cv2
import inference
import uuid


def run(model, image):
    output, _ = inference.inference(model, image)
    
    # write the resulting image to a file
    name = f"/storage/{str(uuid.uuid4())}.jpg"
    cv2.imwrite(name, output)

    return name
