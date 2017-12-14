def write_html( path_list):

    new_list = []
    for i in path_list:
        new_list.append(i.replace('xMINUSx','-').replace('xUNDERx','_')[1:])

    origin = str(new_list[0])
    new_list.remove(origin)
    waypoints = ""
    for p in new_list:
        waypoints += " waypts.push({location: {placeId:'"+p+"'},stopover: true});"

    html = '''<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Waypoints in directions</title>
    <style>
      #right-panel {
        font-family: 'Roboto','sans-serif';
        line-height: 30px;
        padding-left: 10px;
      }

      #right-panel select, #right-panel input {
        font-size: 15px;
      }

      #right-panel select {
        width: 100%;
      }

      #right-panel i {
        font-size: 12px;
      }
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
        float: left;
        width: 100%;
        height: 100%;
      }

    </style>
  </head>
  <body>
    <div id="map"></div>

    </div>
    <script>
      function initMap() {
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer;
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 6,
          center: {lat: 41.85, lng: -87.65}
        });


        directionsDisplay.setMap(map);

          calculateAndDisplayRoute(directionsService, directionsDisplay);

      }

      function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        var waypts = [];
            '''+waypoints+'''




      directionsService.route({
          origin: {placeId: '''+"'"+origin+"'"+''' },
          destination: {placeId: '''+"'"+origin+"'"+'''},
          waypoints: waypts,
          optimizeWaypoints: false,
          travelMode: 'DRIVING'
        }, function(response, status) {
          if (status === 'OK') {
            directionsDisplay.setDirections(response);
            var route = response.routes[0];
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
      }

    </script>
    <script async defer
    src="http://maps.googleapis.com/maps/api/js?key=AIzaSyB70wPQAQR-5P86DJ2j1QcAgYVbR0-xD_k&callback=initMap">
    </script>
  </body>
</html>'''
    return html
