const addToCart = function(event_id){
    var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
        csrf = csrf.value;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/cart/add', true);
        xhr.setRequestHeader('X-CSRFToken', csrf);
        xhr.setRequestHeader('enctype', 'multipart/form-data')
        xhr.getResponseHeader('Content-type', 'application/json');
        xhr.onload = () =>{
            console.log("true");
            if (this.status === 200) {
                console.log(this.responseText);
                showSnackbar(this.responseText,'success',document.body);
            } else {
                console.error("Some error occured");
                showSnackbar(this.responseText,'error',document.body);
            }
        }
        xhr.send(JSON.stringify({
            "event_id": event_id
        }));
}

const deleteFromCart = function(event_id){
    var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
        csrf = csrf.value;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/cart/delete', true);
        xhr.setRequestHeader('X-CSRFToken', csrf);
        xhr.setRequestHeader('enctype', 'multipart/form-data')
        xhr.getResponseHeader('Content-type', 'application/json');
        xhr.onload = () =>{
            console.log("true");
            if (this.status === 200) {
                console.log(this.responseText);
                showSnackbar(this.responseText,'success',document.body);
            } else {
                console.error("Some error occured");
                showSnackbar(this.responseText,'error',document.body);
            }
        }
        xhr.send(JSON.stringify({
            "event_id": event_id
        }));
}

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