async function startFacialRecognition() {
  const video = document.getElementById('video');

  await faceapi.nets.tinyFaceDetector.loadFromUri('/static/models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('/static/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/static/models');

  navigator.mediaDevices.getUserMedia({ video: {} })
    .then(stream => {
      video.srcObject = stream;
      video.play();
    })
    .catch(err => console.error('Error al acceder a la cámara: ', err));

  video.addEventListener('loadeddata', async () => {
    const canvas = faceapi.createCanvasFromMedia(video);
    document.body.append(canvas);
    const displaySize = { width: video.width, height: video.height };
    faceapi.matchDimensions(canvas, displaySize);

    const interval = setInterval(async () => {
      const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptors();
      const resizedDetections = faceapi.resizeResults(detections, displaySize);

      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
      faceapi.draw.drawDetections(canvas, resizedDetections);
      faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

      if (resizedDetections.length > 0) {
        const email = document.getElementById('email').value;
        const faceDescriptor = Array.from(resizedDetections[0].descriptor);
        const match = await sendFaceDescriptor(email, faceDescriptor);
        if (match) {
          clearInterval(interval);
          video.pause();
          alert('Rostro reconocido. Iniciando sesión...');
          window.location.href = '/home';
        } else {
          alert('La cara no coincide con la cara asociada al correo electrónico ingresado.');
        }
      }
    }, 100);
  });
}

async function sendFaceDescriptor(email, faceDescriptor) {
  const response = await fetch('/sign_in_face', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, faceDescriptor }),
  });

  if (response.ok) {
    const result = await response.json();
    return result.success;
  } else {
    alert('Error durante el reconocimiento facial.');
    return false;
  }
}
