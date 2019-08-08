// // Initializing
// window.onload = function(){
//   var dwn = document.getElementById('btndownload'),
//       canvas = document.getElementById('canvas'),
//       context = canvas.getContext('2d');

//   // Event handler for download
//   dwn.onclick = function(){
//     download(canvas, 'myimage.png');
//   }

// }

// /* Canvas Donwload */
// function download(canvas, filename) {
//   /// create an "off-screen" anchor tag
//   var lnk = document.createElement('a'), e;

//   /// the key here is to set the download attribute of the a tag
//   lnk.download = filename;

//   /// convert canvas content to data-uri for link. When download
//   /// attribute is set the content pointed to by link will be
//   /// pushed as "download" in HTML5 capable browsers
//   lnk.href = canvas.toDataURL("image/png;base64");

//   /// create a "fake" click-event to trigger the download
//   if (document.createEvent) {
//     e = document.createEvent("MouseEvents");
//     e.initMouseEvent("click", true, true, window,
//                      0, 0, 0, 0, 0, false, false, false,
//                      false, 0, null);

//     lnk.dispatchEvent(e);
//   } else if (lnk.fireEvent) {
//     lnk.fireEvent("onclick");
//   }
// 

 $(document).ready(function () {
   $("#btn-downloadQR").click(function(){
     downloadImage();
   });
 });

 function downloadImage(){
   html2canvas(document.querySelector("#yes"), {
    windowWidth: document.querySelector("#yes").scrollWidth,
    windowHeight: document.querySelector("#yes").scrollHeight
}).then(canvas => {
    a = document.createElement('a'); 
    document.body.appendChild(a); 
    a.download = "test.png"; 
    a.href =  canvas.toDataURL();
    a.click();
  });  
 }