const addToCart = function(event_id){
    var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
        csrf = csrf.value;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/cart/add', true);
        xhr.setRequestHeader('X-CSRFToken', csrf);
        xhr.setRequestHeader('enctype', 'multipart/form-data')
        xhr.getResponseHeader('Content-type', 'application/json');
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
                showSnackbar(this.responseText,'success',document.body);
            } else if (this.readyState == 4 && this.status != 200) {
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
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
                showSnackbar(this.responseText,'success',document.body);
                window.location.reload();
            }  else if (this.readyState == 4 && this.status != 200) {
                console.error("Some error occured");
                showSnackbar(this.responseText,'error',document.body);
            }
        }
        xhr.send(JSON.stringify({
            "event_id": event_id
        }));
}
