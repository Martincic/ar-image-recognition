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

function scanEnvironment() {
    // Take a photo every 0.5s and upload it
    let interval = setInterval(myTimer, 500);

    // Stop taking photos after 10s, call /processImages API and get the results
    setTimeout(function() { 
        clearInterval(interval); 
        //TODO: Send request to /processImages
        //return response from processed images to the screen
        //draw on map the prediction of where the person is located
    }, 10000);
}

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

    let req = $.ajax({
        type: "POST",
        url: "/uploadImage",
        data: data,
        contentType: 'image/jpeg',
        processData: false,
        success: function (data) {
                console.log('true');
                console.log(data);
        },
        error: function (data) {
            console.log('There was an error uploading your file!');
        }
    }).done(function () {
        console.log("Sent");
    });
}    