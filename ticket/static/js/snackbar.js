const showSnackbar = function(message,tag,element){
    const snackBar = document.createElement('div');
    snackBar.classList.add(tag);
    snackBar.id = 'snackbar';
    snackBar.innerHTML = `${message}
    <span class="btn-outline-${tag} btn-sm closebtn"
      onclick="this.parentElement.style.display='none';">&times;
    </span>`;
    element.appendChild(snackBar);
}