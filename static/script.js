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
    let dest = document.querySelectorAll('.destination');
    let map_path = document.querySelectorAll('.item');

    function points_Off(arr) {
        for (var i = 0; i < arr.length; i++) {
            arr[i].setAttributeNS(null, 'fill', '#0d6efd00');
        }
    }

    points_Off(dots);
    points_Off(dest);

    points_Off(map_path);

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
    let spinner = document.getElementById('spinner');
    let spinner_text = document.getElementById('spinner-text');

    scanBtn.addEventListener("click", scanEnvironment);


    function scanEnvironment() {
        // add spinner
        spinner_text.textContent = '';
        spinner.classList.remove('d-none');
        scanBtn.style.padding = '0.5em 1em';

        // Take a photo every 0.5s and upload it
        let interval = setInterval(myTimer, 500);

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
                    points_Off(dots);
                    dots[sessionStorage.dot_id].setAttributeNS(null, 'fill', '#d74200');

                    // remove spinner
                    scanBtn.style.padding = '1em';
                    spinner.classList.add('d-none');
                    spinner_text.textContent = 'Scan';
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


    function myTimer() {
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
