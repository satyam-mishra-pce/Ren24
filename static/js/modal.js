/* 
Dependecies:
cart.js
snackbar.js
 */


const showModalDialog = (eventid,userId) => {
  var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
  csrf = csrf.value;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/getevent', true);
  xhr.setRequestHeader('X-CSRFToken', csrf);
  xhr.setRequestHeader('enctype', 'multipart/form-data')
  xhr.getResponseHeader('Content-type', 'application/json');
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
      const data = JSON.parse(this.responseText);
      const modal = document.getElementById('modal');
      modal.style.display = 'block';
      document.getElementById('event-name').innerText = data['name'];
      document.getElementById('event-description').innerText = data['desc'];
      document.getElementById('event-amount').innerText = data['amount'];
      if (data['includedInPass'] == true) {
        document.getElementById('event-access').innerText = "Included in ren pass";
      }else{
        document.getElementById('event-access').innerText = "";
        try{
          document.getElementById('buy-now-btn').disabled = true;
        }catch (e){
          console.log(e);
        }
      }
      try{
        document.getElementById('buy-now-btn').addEventListener('click',()=>{
          // addToCart(data['id']);
          // modal.style.display = 'none';
          if(confirm(`Are you sure you want to buy a ticket for ${data['name']}? 
          This will be used from your Ren pass.`) == true){
            window.location = `/buy/${data['id']}`;
          }
        });
      }catch(e){
        console.log(e);
      }
      modal.addEventListener('click',(e)=>{
        let closeBtn = document.getElementById('close-modal-btn');
        if(e.target === modal || e.target === closeBtn){
          modal.style.display = 'none';
        }
      });
      // showSnackbar(this.responseText, 'success', document.body);
    } else if (this.readyState == 4 && this.status != 200) {
      console.error("Some error occured");
      showSnackbar(this.responseText, 'error', document.body);
    }
  }
  xhr.send(JSON.stringify({
    "event_id": eventid,
    'user_id':userId
  }));

}
const showAnonymousModalDialog = (eventid) => {
  var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
  csrf = csrf.value;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/getevent', true);
  xhr.setRequestHeader('X-CSRFToken', csrf);
  xhr.setRequestHeader('enctype', 'multipart/form-data')
  xhr.getResponseHeader('Content-type', 'application/json');
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
      const data = JSON.parse(this.responseText);
      const modal = document.getElementById('modal');
      modal.style.display = 'block';
      document.getElementById('event-name').innerText = data['name'];
      document.getElementById('event-description').innerText = data['desc'];
      document.getElementById('event-amount').innerText = data['amount'];
      if (data['includedInPass'] == true) {
        document.getElementById('event-access').innerText = "Included in ren pass";
      }else{
        document.getElementById('event-access').innerText = "";
        // try{
        //   document.getElementById('buy-now-btn').disabled = true;
        // }catch (e){
        //   console.log(e);
        // }
      }
      // try{
      //   document.getElementById('buy-now-btn').addEventListener('click',()=>{
      //     // addToCart(data['id']);
      //     // modal.style.display = 'none';
      //     if(confirm(`Are you sure you want to buy a ticket for ${data['name']}? 
      //     This will be used from your Ren pass.`) == true){
      //       window.location = `/buy/${data['id']}`;
      //     }
      //   });
      // }catch(e){
      //   console.log(e);
      // }
      modal.addEventListener('click',(e)=>{
        let closeBtn = document.getElementById('close-modal-btn');
        if(e.target === modal || e.target === closeBtn){
          modal.style.display = 'none';
        }
      });
      // showSnackbar(this.responseText, 'success', document.body);
    } else if (this.readyState == 4 && this.status != 200) {
      console.error("Some error occured");
      showSnackbar(this.responseText, 'error', document.body);
    }
  }
  xhr.send(JSON.stringify({
    "event_id": eventid,
  }));

}