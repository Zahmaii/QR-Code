import streamlit as st
import cv2

# Function to capture video feed and detect QR code
def qr_code_detection():
    # Initialize QRCodeDetector
    qr_decoder = cv2.QRCodeDetector()

    # Start webcam feed
    cap = cv2.VideoCapture(0)

    stframe = st.empty()  # Streamlit frame to display video feed

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            st.error("Failed to capture video feed.")
            break

        # Detect and decode the QR code
        data, bbox, _ = qr_decoder.detectAndDecode(frame)

        # If a QR code is detected, draw the bounding box and display the data
        if bbox is not None and len(bbox) > 0:
            n_lines = len(bbox[0])
            for i in range(n_lines):
                # Ensure point1 and point2 are tuples of integers
                point1 = (int(bbox[0][i][0]), int(bbox[0][i][1]))
                point2 = (int(bbox[0][(i + 1) % n_lines][0]), int(bbox[0][(i + 1) % n_lines][1]))
                cv2.line(frame, point1, point2, (0, 255, 0), 2)

            if data:
                # Split the data into separate lines if there are multiple lines
                data_lines = data.split('\n')
                for i, line in enumerate(data_lines):
                    # Display each line of data at a different position
                    cv2.putText(frame, f"Data {i + 1}: {line}", (10, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Stream the video frame to the Streamlit app
        stframe.image(frame, channels="BGR")

        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

# Streamlit page configuration
st.title("QR Code Detection with OpenCV and Streamlit")

st.write("This app uses OpenCV to detect QR codes from your webcam and displays the result in real-time.")

# Button to start QR code detection
if st.button("Start QR Code Detection"):
    qr_code_detection()

st.write("Press the 'Start QR Code Detection' button to start the webcam feed.")