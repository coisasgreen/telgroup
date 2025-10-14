# upload_receipt.py
# Flask + OpenCV image verification server
# Run:  python upload_receipt.py

import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# CONFIG
APPROVED_LOGO_PATH = os.path.join(os.path.dirname(__file__), "approved_logo.png")
ALLOWED_EXT = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

# Load logo
if not os.path.exists(APPROVED_LOGO_PATH):
    raise FileNotFoundError("approved_logo.png not found.")

logo_img = cv2.imread(APPROVED_LOGO_PATH, cv2.IMREAD_GRAYSCALE)
orb = cv2.ORB_create(1000)
logo_kp, logo_des = orb.detectAndCompute(logo_img, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

@app.route("/upload_receipt", methods=["POST"])
def upload_receipt():
    if 'receipt' not in request.files:
        return jsonify(success=False, message="No file uploaded."), 400

    file = request.files['receipt']
    if file.filename == '':
        return jsonify(success=False, message="No file selected."), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify(success=False, message="Invalid file type. Only PNG/JPG allowed."), 400

    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return jsonify(success=False, message="Cannot read image file."), 400

    kp2, des2 = orb.detectAndCompute(img, None)
    if des2 is None:
        return jsonify(success=False, message="No features detected in image."), 200

    matches = bf.knnMatch(logo_des, des2, k=2)
    good = [m for m, n in matches if m.distance < 0.75 * n.distance]

    if len(good) < 10:
        return jsonify(success=False, message="Logo not found on receipt."), 200

    src_pts = np.float32([logo_kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if M is None:
        return jsonify(success=False, message="Logo match unreliable."), 200

    inliers = int(mask.sum())
    if inliers >= 10:
        return jsonify(success=True, message="Logo detected in receipt.")
    else:
        return jsonify(success=False, message="Logo verification failed."), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
