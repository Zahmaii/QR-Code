import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np

st.title("QR Code Scanner")

# Upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Display the image
    st.image(image, channels="BGR")

    # Decode the QR code
    decoded_objects = decode(image)
    for obj in decoded_objects:
        st.write("Type:", obj.type)
        st.write("Data:", obj.data.decode("utf-8"))

        # Draw the rectangle around the QR code
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        for j in range(0, n):
            cv2.line(image, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

    # Display the image with the QR code highlighted
    st.image(image, channels="BGR")
