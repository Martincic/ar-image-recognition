// from https://www.webdevdrops.com/en/how-to-access-device-cameras-with-javascript/

window.addEventListener('DOMContentLoaded', () => {
    if (
        !"mediaDevices" in navigator ||
        !"enumerateDevice" in navigator.mediaDevices
    ) {
        alert("Camera access permissions available in your browser");
        return;
    }


    // TEST SVG MAP
    let dots = document.querySelectorAll('.point');

    function dots_Off() {
        for (var i = 0; i < dots.length; i++) {
            dots[i].setAttributeNS(null, 'fill', '#0d6efd00');
        }
    }
    dots_Off()


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

    let scanBtn = document.getElementById('scanBtn');
    scanBtn.addEventListener("click", scanEnvironment);


    function scanEnvironment() {
        // Take a photo every 0.5s and upload it
        let interval = setInterval(myTimer, 500);
        console.log(dots)
        // dots[0].setAttributeNS(null, 'fill', '#d74200');
        // Stop taking photos after 10s, call /processImages API and get the results
        setTimeout(function () {
            clearInterval(interval);
            //TODO: return response from processed images to the screen
            //TODO: draw on map the prediction of where the person is located
            $.ajax({
                type: "GET",
                url: "/processImages",
                processData: false,
                success: function (data) {

                    console.log(data);
                    data = JSON.parse(data);
                    sessionStorage.dot_id = data.dot_id - 1;
                    alert(data.dot_id);
                    
                    // draw location on map
                    dots_Off();
                    dots[sessionStorage.dot_id].setAttributeNS(null, 'fill', '#d74200');
                    // alert(data);
                },
                error: function (data) {
                    console.log('There was an error uploading your file!');
                }
            }).done(function () {
                console.log("Sent");
            });
        }, 10000);
    }

    let counter = 0;

    function myTimer() {
        counter++;
        document.getElementById('counter').innerHTML = counter;
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');
        var video = document.getElementById('video');
        ctx.drawImage(video, 0, 0)
        ctx.translate(video, 0)

        document.getElementById("canvas").style = "display:none;"
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
});
