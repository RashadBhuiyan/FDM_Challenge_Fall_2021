// Open the Modal
function openModal() {
    document.getElementById("myModal").style.display = "block";
}
  
  // Close the Modal
function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

var lightboxIndex = 1;

function plusLightbox(n) {
    currentLightbox(lightboxIndex += n);
}
function currentLightbox(n) {
    showLightbox(lightboxIndex = n);
}
  
function showLightbox(n) {
    var i;
    var slides = document.getElementsByClassName("lightboxSlides");
    if (n > slides.length) {lightboxIndex = 1}
    if (n < 1) {lightboxIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    slides[lightboxIndex-1].style.display = "block";
}
  