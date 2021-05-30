var overlay = document.getElementById('overlay');

var btnClose = document.getElementById('btnClose');
btnClose.addEventListener('click',closeModal);
function closeModal() {
    overlay.style.display='none';
}

var btnPopup_haute_savoie = document.getElementById('popup-haute-savoie');
btnPopup_haute_savoie.addEventListener('click',showinfo);

var btnPopup_savoie = document.getElementById('popup-savoie');
btnPopup_savoie.addEventListener('click',showinfo);

function showinfo() {
    overlay.style.display='block';
    popup.style.display='block';
    btnClose.style.display='block';
}






