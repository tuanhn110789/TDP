
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
   <!DOCTYPE html>
<html>
<head>
  <title>Nhận diện giấy A4 hình chữ nhật</title>
  https://docs.opencv.org/4.x/opencv.js
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
  <h2>📷 Nhận diện giấy A4 hình chữ nhật bằng Camera</h2>
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
          let gray = new cv.Mat();
          let edges = new cv.Mat();
          let contours = new cv.MatVector();
          let hierarchy = new cv.Mat();

          cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
          cv.GaussianBlur(gray, gray, new cv.Size(5, 5), 0);
          cv.Canny(gray, edges, 50, 150);
          cv.findContours(edges, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);

          for (let i = 0; i < contours.size(); ++i) {
            let cnt = contours.get(i);
            let approx = new cv.Mat();
            cv.approxPolyDP(cnt, approx, 0.02 * cv.arcLength(cnt, true), true);

            if (approx.rows === 4 && cv.isContourConvex(approx)) {
              let rect = cv.boundingRect(approx);
              let aspectRatio = rect.width / rect.height;
              if (aspectRatio > 0.65 && aspectRatio < 0.75) {
                cv.drawContours(src, contours, i, new cv.Scalar(0, 255, 0, 255), 3);
                let corners = [];
                for (let j = 0; j < 4; j++) {
                  let point = approx.intPtr(j);
                  corners.push({ x: point[0], y: point[1] });
                  cv.circle(src, new cv.Point(point[0], point[1]), 5, new cv.Scalar(255, 0, 255, 255), -1);
                }
                console.log("📐 Tọa độ 4 góc giấy A4:", corners);
              }
            }

            approx.delete();
            cnt.delete();
          }

          cv.imshow('canvas', src);
          src.delete(); gray.delete(); edges.delete(); contours.delete(); hierarchy.delete();
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




