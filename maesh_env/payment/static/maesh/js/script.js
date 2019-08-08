//If clicked on download QR button
$(document).ready(function () {
  $("#downloadQR").click(function(){
    downloadQR();
  });
});

//Download the QR function
function downloadQR(){
  var screen = document.querySelector("#screen");
  html2canvas(screen, {
    windowWidth: screen.scrollWidth,
    windowHeight: screen.scrollHeight
}).then(canvas => {
    a = document.createElement('a'); 
    document.body.appendChild(a); 
    a.download = "test.png"; 
    a.href =  canvas.toDataURL();
    a.click();
  });  
}