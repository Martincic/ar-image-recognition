// from https://www.webdevdrops.com/en/how-to-access-device-cameras-with-javascript/

(function () {
    if (
        !"mediaDevices" in navigator ||
        !"enumerateDevice" in navigator.mediaDevices
    ) {
        alert("Camera access permissions available in your browser");
        return;
    }

    // get page elements
    const video = document.querySelector("#video");

    // video constraints
    const constraints = {
        audio: false,
        video: {
            facingMode: { 
                exact: "environment"
            },
            width: {
                min: 1024,
                ideal: 1280,
                max: 1920,
            },
            height: {
                min: 576,
                ideal: 720,
                max: 1080,
            },
        },
    };

    // current video stream
    let videoStream;

    // stop video stream
    function stopVideoStream() {
        if (videoStream) {
            videoStream.getTracks().forEach((track) => {
                track.stop();
            });
        }
    }

    // initialize
    async function initializeCamera() {
        stopVideoStream();
        try {
            videoStream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = videoStream;
        } catch (err) {
            alert("Could not access the camera");
        }
    }

    initializeCamera();
})();