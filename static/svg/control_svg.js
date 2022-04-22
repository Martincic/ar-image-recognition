window.addEventListener('DOMContentLoaded', () => {
    console.log('aaa');

    points = document.querySelectorAll('.point');

    function colorCountries(data, color) {
        for (var i = 0; i < data.length; i++){
            data[i].setAttributeNS(null, 'fill', color);
        }
    }

    colorCountries(points, '#d74200');
});

