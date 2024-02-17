// Get all the modal trigger elements
const modalTriggers = document.querySelectorAll(".modal-trigger");

// Loop through each modal trigger element and add a click event listener to it
modalTriggers.forEach(function(trigger) {
  // Get the target modal element based on the data-target attribute of the trigger
  const targetModal = document.getElementById(trigger.dataset.target);
  
  // Get the close button element inside the target modal
  const closeBtn = targetModal.querySelector(".close");

  // When the user clicks the trigger, open the target modal
  trigger.addEventListener("click", function() {
    targetModal.style.display = "block"; // Show the target modal
  });

  // When the user clicks the close button or anywhere outside the target modal, close it
  targetModal.addEventListener("click", function(event) {
    if (event.target === targetModal || event.target === closeBtn) {
      targetModal.style.display = "none"; // Hide the target modal
    }
  });
});
