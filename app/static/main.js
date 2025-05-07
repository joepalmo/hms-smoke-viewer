// // static/main.js
// mapboxgl.accessToken = 'pk.eyJ1IjoidGFtbXl6aGFuZyIsImEiOiJjbGd3aWtmYTIwYzdjM3BtdTI1ZHB2dzFoIn0.p02qxsD8C6vO6WdLTwQcug';

// var map = new mapboxgl.Map({
//     container: 'map',
//     style: 'mapbox://styles/mapbox/streets-v11',
//     center: [-98.5, 39.5],
//     zoom: 4
// });

// // Load fire data
// fetch('/data/fire')
//     .then(response => response.json())
//     .then(data => {
//         map.addSource('fireData', {
//             'type': 'geojson',
//             'data': data
//         });

//         map.addLayer({
//             'id': 'fire-layer',
//             'type': 'fill',
//             'source': 'fireData',
//             'paint': {
//                 'fill-color': '#FF0000',
//                 'fill-opacity': 0.5
//             }
//         });
//     });

// // Load smoke data
// fetch('/data/smoke')
//     .then(response => response.json())
//     .then(data => {
//         map.addSource('smokeData', {
//             'type': 'geojson',
//             'data': data
//         });

//         map.addLayer({
//             'id': 'smoke-layer',
//             'type': 'fill',
//             'source': 'smokeData',
//             'paint': {
//                 'fill-color': '#000000',
//                 'fill-opacity': 0.5
//             }
//         });
//     });
