
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
  <script async src="https://docs.opencv.org/4.x/opencv.js" type="text/javascript"></script>
  <style>
    video, canvas {
      max-width: 100%;
      border: 1px solid black;
    }
  </style>
</head>
<body>
  <h2>Camera iPhone - Nhận diện giấy A4 hình chữ nhật</h2>
  <video id="video" autoplay playsinline></video>
  <canvas id="canvas"></canvas>

  <script>
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
      });

    cv['onRuntimeInitialized'] = () => {
      const processFrame = () => {
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

          if (approx.rows === 4) {
            let isRectangle = true;
            for (let j = 0; j < 4; j++) {
              let pt1 = approx.intPtr(j);
              let pt2 = approx.intPtr((j + 1) % 4);
              let pt3 = approx.intPtr((j + 2) % 4);

              let v1 = { x: pt2[0] - pt1[0], y: pt2[1] - pt1[1] };
              let v2 = { x: pt3[0] - pt2[0], y: pt3[1] - pt2[1] };

              let dot = v1.x * v2.x + v1.y * v2.y;
              let mag1 = Math.sqrt(v1.x * v1.x + v1.y * v1.y);
              let mag2 = Math.sqrt(v2.x * v2.x + v2.y * v2.y);
              let angle = Math.acos(dot / (mag1 * mag2)) * (180 / Math.PI);

              if (Math.abs(angle - 90) > 15) {
                isRectangle = false;
                break;
              }
            }

            if (isRectangle) {
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
                console.log("Tọa độ 4 góc giấy A4 hình chữ nhật:", corners);
              }
            }
          }

          approx.delete();
          cnt.delete();
        }

        cv.imshow('canvas', src);
        src.delete(); gray.delete(); edges.delete(); contours.delete(); hierarchy.delete();
        requestAnimationFrame(processFrame);
      };

      processFrame();
    };
  </script>
</body>
</html>

    """

@app.get("/main")
async def root():
    return {"message": "Hoang Tuan"}       


#uvicorn.run(app, host="0.0.0.0", port=90)


