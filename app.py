from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import os

app = Flask(__name__)

# Create the static folder if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture_image():
    try:
        # Initialize the webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return jsonify({"error": "Webcam could not be accessed"}), 500

        # Capture one frame
        ret, frame = cap.read()

        if ret:
            # Save the frame as an image in the static folder
            image_path = "static/captured_image.jpg"
            cv2.imwrite(image_path, frame)
            cap.release()
            return jsonify({"message": "Image captured successfully", "image_path": image_path}), 200
        else:
            cap.release()
            return jsonify({"error": "Failed to capture image"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
