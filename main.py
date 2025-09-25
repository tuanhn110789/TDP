
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
  <!DOCTYPE html>
<html>
<head>
  <title>Nhận diện vật màu trắng như giấy</title>
  <script async src="https://docs.opencv.org/4t>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
    }
    video, canvas {
      max-width: 100%;
      border: 1px solid black;
      margin-top: 10px;
    }
    #controls {
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <h2>📷 Nhận diện vật màu trắng như giấy</h2>
  <div id="controls">
    <button id="switchCameraBtn">🔄 Chuyển camera trước/sau</button>
  </div>
  <video id="video" autoplay playsinline></video>
  <canvas id="canvas"></canvas>

  <script>
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const switchCameraBtn = document.getElementById('switchCameraBtn');

    let currentStream;
    let useFrontCamera = true;

    function stopStream() {
      if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
      }
    }

    function startCamera() {
      stopStream();
      const constraints = {
        video: {
          facingMode: useFrontCamera ? 'user' : 'environment'
        }
      };
      navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
          currentStream = stream;
          video.srcObject = stream;
        })
        .catch(err => {
          console.error("Không thể truy cập camera:", err);
        });
    }

    switchCameraBtn.onclick = () => {
      useFrontCamera = !useFrontCamera;
      startCamera();
    };

    startCamera();

    cv['onRuntimeInitialized'] = () => {
      const processFrame = () => {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

          let src = cv.imread(canvas);
          let hsv = new cv.Mat();
          let mask = new cv.Mat();
          let contours = new cv.MatVector();
          let hierarchy = new cv.Mat();

          // Chuyển sang HSV để dễ lọc màu trắng
          cv.cvtColor(src, hsv, cv.COLOR_RGBA2RGB);
          cv.cvtColor(hsv, hsv, cv.COLOR_RGB2HSV);

          // Ngưỡng màu trắng (có thể điều chỉnh nếu ánh sáng thay đổi)
          let lowWhite = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [0, 0, 200, 0]);
          let highWhite = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [180, 30, 255, 255]);
          cv.inRange(hsv, lowWhite, highWhite, mask);

          // Tìm contour vùng trắng
          cv.findContours(mask, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);

          let maxArea = 0;
          let maxContour = null;

          for (let i = 0; i < contours.size(); ++i) {
            let cnt = contours.get(i);
            let area = cv.contourArea(cnt);
            if (area > maxArea) {
              maxArea = area;
              maxContour = cnt;
            }
          }

          if (maxContour && maxArea > 10000) {
            let approx = new cv.Mat();
            cv.approxPolyDP(maxContour, approx, 0.02 * cv.arcLength(maxContour, true), true);
            cv.drawContours(src, new cv.MatVector([approx]), -1, new cv.Scalar(0, 255, 0, 255), 3);

            let corners = [];
            for (let j = 0; j < approx.rows; j++) {
              let point = approx.intPtr(j);
              corners.push({ x: point[0], y: point[1] });
              cv.circle(src, new cv.Point(point[0], point[1]), 5, new cv.Scalar(255, 0, 255, 255), -1);
            }

            console.log("📐 Tọa độ vùng trắng:", corners);
            approx.delete();
          }

          cv.imshow('canvas', src);
          src.delete(); hsv.delete(); mask.delete(); contours.delete(); hierarchy.delete(); lowWhite.delete(); highWhite.delete();
        }

        requestAnimationFrame(processFrame);
      };

      processFrame();
    };
  </script>
</body>
</html>



    """

@app.get("/main")
async def main():
    return {"message": "Hoang Tuan"}       


#uvicorn.run(app, host="0.0.0.0", port=90)





