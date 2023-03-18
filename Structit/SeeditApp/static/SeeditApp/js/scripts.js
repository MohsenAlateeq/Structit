// When click the dropdown button 
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close dropdown menu if user clicks outside
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// Initialize.
function initMap() {
  // Location.
  const uluru = { lat: 24.6938678, lng: 46.681857 };
  // Map it self and zoom ratio.
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: uluru,
  });
  // Marker
  const marker = new google.maps.Marker({
    position: uluru,
    map: map,
  });
}

window.initMap = initMap;

