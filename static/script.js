// static/script.js
document.addEventListener('DOMContentLoaded', function () {
  // Function to perform WebRTC test
  function performWebRTC() {
    var peerConnection = new RTCPeerConnection({
      iceServers: [{
        urls: "stun:stun.l.google.com:19302"
      }]
    });

    var dataChannel = peerConnection.createDataChannel("test");
    var localIPs = [];

    peerConnection.onicecandidate = function (event) {
      if (event.candidate) {
         var ipMatch = event.candidate.candidate.match(/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/);
        if (ipMatch) {
            var ip = ipMatch[1];
          if(localIPs.indexOf(ip) === -1){
           localIPs.push(ip);
         }
        }
      }
    };
     
    peerConnection.createOffer()
    .then(offer => peerConnection.setLocalDescription(offer))
    .catch(e => console.error("Error creating offer: ", e));
    setTimeout(function() {
        if(localIPs.length > 0) {
           fetch('/webrtc', {
             method: 'POST',
            headers: {
                'Content-Type': 'application/json',
             },
            body: JSON.stringify({local_ip: localIPs[0]}),
          })
           .then(response => response.json())
           .then(data => {
             document.getElementById('webrtc-result').innerText = data.result;
          })
        .catch(error => {
            console.error("Error during WebRTC test:", error);
              document.getElementById('webrtc-result').innerText = 'Error';
          });
        }
      
       peerConnection.close();

    }, 3000)
  }
  performWebRTC();
   // Function to get browser's timezone and time
   function getBrowserTimeAndTime() {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const now = new Date();
      const formattedTime = now.toLocaleString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          timeZoneName: 'short',
          timeZone: timezone
      });

      fetch("/", {
          method: "POST",
          headers: {
              "Content-Type": "application/x-www-form-urlencoded"
          },
          body:  "browser_time=" + formattedTime
      }).then(res => {
           console.log("timezone and time has been posted")
      }).catch(error => {
            console.error("Error sending browser timezone and time:", error);
      })
  }
  getBrowserTimeAndTime();

  // Function to initialize map
  function initMap() {
       fetch('https://api.ipify.org?format=json', {timeout: 5000})
        .then(response => {
            if(!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`)
            }
             return response.json()
           })
           .then(data => {
                const ipAddress = data.ip;
                  fetch(`http://ip-api.com/json/${ipAddress}`, {timeout: 5000})
                     .then(response => {
                          if(!response.ok) {
                              throw new Error(`HTTP error! status: ${response.status}`)
                          }
                          return response.json()
                     })
                     .then(data => {
                          if (data.lat && data.lon) {
                              const latitude = data.lat;
                              const longitude = data.lon;

                              var map = L.map('map', {
                                   zoomAnimation: false,
                                  minZoom: 2,
                                  maxZoom: 18,
                               }).setView([latitude, longitude], 10);

                                L.tileLayer('https://tile.openstreetmap.jp/{z}/{x}/{y}.png', {
                                 attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                 }).addTo(map);

                                L.marker([latitude, longitude]).addTo(map)
                                .bindPopup(`Your IP location is approximately here.`);

                          } else {
                              console.error("Could not get lat/long from API");
                              document.getElementById('map').innerText = 'Could not fetch map information';
                          }
                       })
                    .catch(error => {
                       console.error("Error fetching location:", error);
                        document.getElementById('map').innerText = 'Could not fetch map information';
                  });
         })
          .catch(error => {
               console.error("Error fetching ip:", error);
               document.getElementById('map').innerText = 'Could not fetch map information';
          })

    }


  initMap();
});