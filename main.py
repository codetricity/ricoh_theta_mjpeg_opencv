import requests
from requests.auth import HTTPDigestAuth
import cv2
import numpy as np

url = "http://[Camera IP Address]/osc/commands/execute"
username = "CameraSerialNumber"
password = "DigitsOnlyofCameraSerialNumber"

# example information
# url = 'http://192.168.2.101/osc/commands/execute'
# username = "THETAYL00105377"
# password = "00105377"

payload = {
    "name": "camera.getLivePreview"
}

headers = {
    "Content-Type": "application/json;charset=utf-8"
}

response = requests.post(url, auth=HTTPDigestAuth(username, password), json=payload, headers=headers, stream=True)

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
                cv2.imshow("Preview", img)
                if cv2.waitKey(1) == 27:
                    break
else:
    print("Error: ", response.status_code)

cv2.destroyAllWindows()
