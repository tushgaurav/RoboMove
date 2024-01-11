import cv2


def OverlayLogo(logo, img, scale_percent, x_offset, y_offset):
    imgLogo = cv2.imread(logo, cv2.IMREAD_UNCHANGED)
    scale_percent = scale_percent  # percentage of original size
    width = int(imgLogo.shape[1] * scale_percent / 100)
    height = int(imgLogo.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_imgLogo = cv2.resize(imgLogo, dim, interpolation=cv2.INTER_AREA)

    imgLogo_img = resized_imgLogo[:, :, :3]  # Color channels
    alpha = resized_imgLogo[:, :, 3] / 255.0  # Normalized alpha channel

    y1, y2 = y_offset, y_offset + imgLogo_img.shape[0]
    x1, x2 = x_offset, x_offset + imgLogo_img.shape[1]

    for c in range(0, 3):
        img[y1:y2, x1:x2, c] = (alpha * imgLogo_img[:, :, c] +
                                (1 - alpha) * img[y1:y2, x1:x2, c])

    return img


def fpsOverlay(fps, img):
    """
    Overlays the FPS on the given image.

    Args:
    img (numpy.ndarray): The image on which to overlay the text.
    fps (float): The frames per second value to display.

    Returns:
    numpy.ndarray: The image with FPS text overlay.
    """
    # Define the font, scale, thickness, and color of the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (5, 250, 0)  # Blue color in BGR
    line_type = 2

    # Format the FPS to two decimal places
    fps_text = f'FPS: {fps:.2f}'

    # Position of the text
    position = (20, 90)

    # Overlay the text on the image
    cv2.putText(img, fps_text, position, font,
                font_scale, font_color, line_type)

    return img


def fpsOverlayHighContrast(fps, img):
    """
    Overlays the FPS on the given image with a cooler style.

    Args:
    img (numpy.ndarray): The image on which to overlay the text.
    fps (float): The frames per second value to display.

    Returns:
    numpy.ndarray: The image with FPS text overlay.
    """
    # Define the font, scale, thickness, and color of the text
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_color = (0, 255, 255)  # Yellow color in BGR
    background_color = (0, 0, 0)  # Black background for better visibility
    line_type = 2

    # Format the FPS to two decimal places
    fps_text = f'FPS: {fps:.2f}'

    # Position of the text
    position = (1600, 50)

    # Calculate text size and position
    (text_width, text_height), _ = cv2.getTextSize(
        fps_text, font, font_scale, line_type)
    text_offset_x, text_offset_y = position
    box_coords = ((text_offset_x, text_offset_y + 5),
                  (text_offset_x + text_width, text_offset_y - text_height - 5))

    # Draw the background box for text
    cv2.rectangle(img, box_coords[0], box_coords[1],
                  background_color, cv2.FILLED)

    # Overlay the text on the image
    cv2.putText(img, fps_text, position, font,
                font_scale, font_color, line_type)

    return img
