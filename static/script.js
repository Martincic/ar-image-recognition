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


setInterval(myTimer, 5000);
let counter = 0;

function myTimer() {
    counter++;
    document.getElementById('counter').innerHTML = counter;
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var video = document.getElementById('video');
    ctx.drawImage(video,0,0)
    ctx.translate(video,0)

    // var c = document.getElementById("canvas");
    // var ctx = c.getContext("2d");
    // ctx.fillStyle = "#FF0000";
    // ctx.fillRect(20, 20, 150, 100);

    document.getElementById("canvas").style = "display:none;"
    //ctx.drawImage(canvas,0,0)
    data = canvas.toDataURL("image/JPEG");

    console.log(data)
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/maskImage", //I have doubt about this url, not sure if something specific must come before "/take_pic"
        data: imgURL,
        success: function(data) {
          if (data.success) {
            alert('Your file was successfully uploaded!');
          } else {
            alert('There was an error uploading your file!');
          }
        },
        error: function(data) {
          alert('There was an error uploading your file!');
        }
      }).done(function() {
        console.log("Sent");
      });
}    