import cv2

def check_connected_cameras(max_index=10):
    """
    Checks for cameras connected to the system up to a specified maximum index.
    :param max_index: The maximum camera index to check.
    :return: List of available camera indexes.
    """
    available_cameras = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            available_cameras.append(i)
            cap.release()
        else:
            print(f"No camera found at index {i}")
    
    return available_cameras

# Check for connected cameras up to index 10
available_cameras = check_connected_cameras(10)
print("Available Cameras:", available_cameras)
