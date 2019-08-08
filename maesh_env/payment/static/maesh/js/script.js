//If clicked on download QR button
$(document).ready(function () {
  $("#downloadQR").click(function(){
    downloadQR();
  });
});

//Download the QR function
function downloadQR(){
  var screen = document.querySelector("#screen");
  var qr = document.querySelector("#qrsvg");
  html2canvas(qr, {
    windowWidth: screen.scrollWidth,
    windowHeight: screen.scrollHeight,
}).then(canvas => {
    // a = document.createElement('a'); 
    // document.body.appendChild(a); 
    // a.download = "maesh_qr.png"; 
    // a.href =  canvas.toDataURL();
    // a.click();
    $( "#qrsvg" ).replaceWith(canvas.toDataURL());
  });  
}