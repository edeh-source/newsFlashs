import cv2
import numpy as np



def resize_and_add_text(image_path, output_path, text="ZenBlog"):
    """
    A method to resize an image and write a text on it
    """
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (900, 500), interpolation=cv2.INTER_AREA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_color = (0, 0, 255)
    thickness = 2
    position = (0, 40)

    #add a rectangle behind the text for better visibiltity
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x, text_y = position
    rectangle_bkg = (0, 0, 0)
    cv2.rectangle(
            resized_image, (text_x - 10, text_y - text_size[1] - 10),
            (text_x + text_size[0] + 10, text_y + 10),
            rectangle_bkg, -1,

        )
    cv2.putText(resized_image, text, position, font, font_scale, font_color, thickness)
    cv2.imwrite(output_path, resized_image)
