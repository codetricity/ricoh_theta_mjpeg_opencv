import requests
from requests.auth import HTTPDigestAuth
import cv2
import numpy as np

# url = "http://[Camera IP Address]/osc/commands/execute"
# username = "CameraSerialNumber"
# password = "DigitsOnlyofCameraSerialNumber"

# example information
# url = 'http://192.168.2.101/osc/commands/execute'
# username = "THETAYR14010001"
# password = "14010001"

# access point mode
url = 'http://192.168.1.1/osc/commands/execute'


payload = {
    "name": "camera.getLivePreview"
}

headers = {
    "Content-Type": "application/json;charset=utf-8"
}

# response = requests.post(url, auth=HTTPDigestAuth(username, password), json=payload, headers=headers, stream=True)
response = requests.post(url, json=payload, headers=headers, stream=True)

# showWindow 1: normal view
# showWindow 2: canny edge detection
showWindow = 2

if response.status_code == 200:
    bytes_ = bytes()
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            bytes_ += chunk
            a = bytes_.find(b'\xff\xd8')
            b = bytes_.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_[a:b+2]
                bytes_ = bytes_[b+2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                if (showWindow == 1):
                    cv2.imshow("Preview", img)

                if (showWindow == 2):
                    # Convert to graycsale
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # Blur the image for better edge detection
                    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
                    # Canny Edge Detection
                    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
                    # Display Canny Edge Detection Image
                    cv2.imshow('Canny Edge Detection', edges)                

                # ESC key will quit
                if cv2.waitKey(1) == 27:
                    break



else:
    print("Error: ", response.status_code)

cv2.destroyAllWindows()
