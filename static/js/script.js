document.onclick = function(){
    document.getElementById('myPopup_aide').classList.remove('show');
    document.getElementById('myPopup-haute-savoie').classList.remove('show');
    document.getElementById('myPopup-savoie').classList.remove('show');
    document.getElementById('myPopup-ain').classList.remove('show');
    document.getElementById('myPopup-isere').classList.remove('show');
};


function myFunction_haute_savoie(e) {
    document.getElementById('myPopup-savoie').classList.remove('show');
    document.getElementById('myPopup-ain').classList.remove('show');
    document.getElementById('myPopup-isere').classList.remove('show');

    var popup = document.getElementById("myPopup-haute-savoie");
    popup.classList.toggle("show");
    e.stopPropagation();
}


function myFunction_savoie(e) {
    document.getElementById('myPopup-ain').classList.remove('show');
    document.getElementById('myPopup-haute-savoie').classList.remove('show');
    document.getElementById('myPopup-isere').classList.remove('show');

    var popup = document.getElementById("myPopup-savoie");
    popup.classList.toggle("show");
    e.stopPropagation();
}


function myFunction_ain(e) {
    document.getElementById('myPopup-haute-savoie').classList.remove('show');
    document.getElementById('myPopup-savoie').classList.remove('show');
    document.getElementById('myPopup-isere').classList.remove('show');

    var popup = document.getElementById("myPopup-ain");
    popup.classList.toggle("show");
    e.stopPropagation();
}


function myFunction_isere(e) {
    document.getElementById('myPopup-haute-savoie').classList.remove('show');
    document.getElementById('myPopup-savoie').classList.remove('show');
    document.getElementById('myPopup-ain').classList.remove('show');

    var popup = document.getElementById("myPopup-isere");
    popup.classList.toggle("show");
    e.stopPropagation();
}



function myFunction_aide(e) {
    var popup = document.getElementById("myPopup_aide");
    popup.classList.toggle("show");
    e.stopPropagation();
}


function generatePDF() {
    // Choose the element that our invoice is rendered in.
    const element = document.getElementById("invoice");
    // Choose the element and save the PDF for our user.
    html2pdf()
      .from(element)
      .save();
  }