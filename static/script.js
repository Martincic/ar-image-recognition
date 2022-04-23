import * as Map from './map.js';
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
            // alert("Could not access the camera");
            console.log("Could not access the camera");
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

        // store destination
        sessionStorage.dest_id = document.getElementById('sel1').value;
        console.log('selected destination: ', sessionStorage.dest_id);

        // Take a photo every 0.5s and upload it
        let interval = setInterval(myTimer, 500);

        // Stop taking photos after 10s, call /processImages API and get the results
        setTimeout(function () {
            clearInterval(interval);
            $.ajax({
                type: "GET",
                url: "/processImages",
                processData: false,
                success: function (data) {

                    data = JSON.parse(data);
                    sessionStorage.dot_id = data.dot_id - 1;
                    console.log(data.dot_id);
                    let coords = Map.getCoordinatesForRoute(String(data.dot_id), String(sessionStorage.dest_id));
                    drawLines(coords);
                    // draw location on map
                    points_Off(dots);
                    points_Off(dest);
                    dots[sessionStorage.dot_id].setAttributeNS(null, 'fill', '#d74200');
                    document.getElementById(sessionStorage.dest_id).setAttributeNS(null, 'fill', '#FFFFFF');

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
        }, 1000);
    }


    function drawLines(coords) {
        $("#Layer_1").find('.delete').remove();
        for (let index = 0; index < coords.length-1; index++) {
            const element = coords[index];
            const next = coords[index+1];
            var newLine = document.createElementNS('http://www.w3.org/2000/svg','line');
            newLine.setAttribute('class', 'delete');
            newLine.setAttribute('x1', element.x);
            newLine.setAttribute('y1', element.y);
            newLine.setAttribute('x2', next.x);
            newLine.setAttribute('y2', next.y);
            newLine.setAttribute("stroke", "black")
            $("#Layer_1").append(newLine);
        }
    }

    function myTimer() {
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');
        var video = document.getElementById('video');
        ctx.drawImage(video, 0, 0)
        ctx.translate(video, 0)

        document.getElementById("canvas").style = "display:none;"
        let data = canvas.toDataURL("image/JPEG");

        let req = $.ajax({
            type: "POST",
            url: "/uploadImage",
            data: data,
            contentType: 'image/jpeg',
            processData: false,
            success: function (data) {
            },
            error: function (data) {
                console.log('There was an error uploading your file!');
            }
        }).done(function () {
            console.log("Sent");
        });
    }
});
