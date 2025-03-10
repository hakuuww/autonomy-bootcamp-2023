"""
BOOTCAMPERS TO COMPLETE.

Detects landing pads.
"""
import pathlib

import numpy as np
import torch
import ultralytics

from .. import bounding_box


# This is just an interface
# pylint: disable=too-few-public-methods
class DetectLandingPad:
    """
    Contains the YOLOv8 model for prediction.
    """
    __create_key = object()

    # ============
    # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
    # ============

    # Chooses the GPU if it exists, otherwise runs on the CPU
    # If you have a CUDA capable GPU but want to force it to
    # run on the CPU instead, replace the right side with "cpu"
    __DEVICE = 0 if torch.cuda.is_available() else "cpu"

    # ============
    # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
    # ============

    __MODEL_NAME = "best-2n.pt"

    @classmethod
    def create(cls, model_directory: pathlib.Path):
        """
        model_directory: Directory to models.
        """
        if not model_directory.is_dir():
            return False, None

        model_path = pathlib.PurePosixPath(
            model_directory,
            cls.__MODEL_NAME,
        )

        try:
            model = ultralytics.YOLO(str(model_path))
        # Library can throw any exception
        # pylint: disable-next=broad-exception-caught
        except Exception:
            return False, None

        return True, DetectLandingPad(cls.__create_key, model)

    def __init__(self, class_private_create_key, model: ultralytics.YOLO):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DetectLandingPad.__create_key, "Use create() method"

        self.__model = model

    def run(self, image: np.ndarray) -> "tuple[list[bounding_box.BoundingBox], np.ndarray]":
        """
        Converts an image into a list of bounding boxes.

        image: The image to run on.

        Return: A tuple of (list of bounding boxes, annotated image) .
            The list of bounding boxes can be empty.
        """
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Ultralytics has documentation and examples

        # Use the model's predict() method to run inference
        # Parameters of interest:
        # * source
        # * conf
        # * device
        # * verbose
        # https://docs.ultralytics.com/usage/cfg/#train
        # source is the source directory for images or videos
        # conf is  	object confidence threshold for detection
        # set device to cpu since we don't have gpu???
        # no verbose option in current version
        # a list with a single object is returned since we are only predicting one image
        predictions = self.__model.predict(
            source = image, 
            conf = 0.7, 
            device = self.__DEVICE, 
            boxes = True, 
            verbose = False,
        )

        # Get the Result object
        #There is only one result in the list so we use [0]

        prediction = predictions[0]

        # Plot the annotated image from the Result object
        # Include the confidence value
        image_annotated = prediction.plot(conf=True)

        # Get the xyxy boxes list from the Boxes object in the Result object
        boxes_xyxys = prediction.boxes.xyxy

        # Detach the xyxy boxes to make a copy,
        #There is no detatch in the documentation
  
        # move the copy into CPU space,
        # and convert to a numpy array
        boxes_cpu = boxes_xyxys.detatch().cpu().numpy()



        # Loop over the boxes list and create a list of bounding boxes
        bounding_boxes = []


        #Create method will call the init method, returns a tuple indicating success or failure and the boundingbox object created
        #takes in the bounds, the bounds are in the form of x1y1x2y2
        for box in boxes_cpu:
            
            result, box = bounding_box.BoundingBox.create(box)
            if result:
                bounding_boxes.append(box)
            else:
                return [], image_annotated
        
        return bounding_boxes, image_annotated

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
