// document.getElementById("show-tech").addEventListener("click", function() {
//     document.getElementById("tech").className = "visible-section";
//     document.getElementById("cultural").className = "hidden-section";
//     document.getElementById("splash").className = "hidden-section";
// });

// document.getElementById("show-cultural").addEventListener("click", function() {
//     document.getElementById("tech").className = "hidden-section";
//     document.getElementById("cultural").className = "visible-section";
//     document.getElementById("splash").className = "hidden-section";

// });
// document.getElementById("show-splash").addEventListener("click", function() {
//     document.getElementById("tech").className = "hidden-section";
//     document.getElementById("cultural").className = "hidden-section";
//     document.getElementById("splash").className = "visible-section";
// });
// document.getElementById("show-day1").addEventListener("click", function() {
//     document.getElementById("day1").className = "visible-section";
//     document.getElementById("day2").className = "hidden-section";
//     document.getElementById("day3").className = "hidden-section";
// });

// document.getElementById("show-day2").addEventListener("click", function() {
//     document.getElementById("day1").className = "hidden-section";
//     document.getElementById("day2").className = "visible-section";
//     document.getElementById("day3").className = "hidden-section";

// });
// document.getElementById("show-day3").addEventListener("click", function() {
//     document.getElementById("day1").className = "hidden-section";
//     document.getElementById("day2").className = "hidden-section";
//     document.getElementById("day3").className = "visible-section";
// });
// document.getElementById("show-day01").addEventListener("click", function() {
//     document.getElementById("day01").className = "visible-section";
//     document.getElementById("day02").className = "hidden-section";
//     document.getElementById("day03").className = "hidden-section";
// });

// document.getElementById("show-day02").addEventListener("click", function() {
//     document.getElementById("day01").className = "hidden-section";
//     document.getElementById("day02").className = "visible-section";
//     document.getElementById("day03").className = "hidden-section";

// });
// document.getElementById("show-day03").addEventListener("click", function() {
//     document.getElementById("day01").className = "hidden-section";
//     document.getElementById("day02").className = "hidden-section";
//     document.getElementById("day03").className = "visible-section";
// });
// document.getElementById("show-day001").addEventListener("click", function() {
//     document.getElementById("day001").className = "visible-section";
//     document.getElementById("day002").className = "hidden-section";
//     document.getElementById("day003").className = "hidden-section";
// });

// document.getElementById("show-day002").addEventListener("click", function() {
//     document.getElementById("day001").className = "hidden-section";
//     document.getElementById("day002").className = "visible-section";
//     document.getElementById("day003").className = "hidden-section";

// });
// document.getElementById("show-day003").addEventListener("click", function() {
//     document.getElementById("day001").className = "hidden-section";
//     document.getElementById("day002").className = "hidden-section";
//     document.getElementById("day003").className = "visible-section";
// });

const showModalDialog = (eventid)=>{
  const e = document.getElementById('background_img');
  const modal = document.createElement('div');
  modal.id = 'modal';
  modal.classList.add("modal-overlay");
  modal.style.display = 'block';
  e.appendChild(modal);
  var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
        csrf = csrf.value;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/getevent', true);
        xhr.setRequestHeader('X-CSRFToken', csrf);
        xhr.setRequestHeader('enctype', 'multipart/form-data')
        xhr.getResponseHeader('Content-type', 'application/json');
        xhr.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
                const data = JSON.parse(this.responseText);
                let str = '';
                 if (data['includedInPass'] == true) {
                  str = `<h4 class="my-2" style="color:red;">Included in Ren Pass</h4>`;
                 }
                modal.innerHTML =   `
      <div class="modal-body">
        <div class="d-flex justify-content-between">
          <h2>${data['name']}</h2>
          <button class="btn btn-outline-danger my-auto" onclick="closeModal(this)">&times;</button>
        </div>
        <p>${data['desc']}</p>
        <h4 class="my-2">Amount</h4>
        <span>${data['amount']}</span>
        ${str}
        <br><button class="btn-primary" onclick="addToCart(${data['id']})">Add to cart</button>
      </div>`;
                showSnackbar(this.responseText,'success',document.body);
            } else {
                console.error("Some error occured");
                showSnackbar(this.responseText,'error',document.body);
            }
        }
        xhr.send(JSON.stringify({
            "event_id": eventid
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
