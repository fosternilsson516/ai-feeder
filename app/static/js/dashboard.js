document.addEventListener('DOMContentLoaded', function () {
    // Add event listener to the document for clicks on the menu button
    document.addEventListener('click', function(event) {
      const menuBtn = document.querySelector('.menu-btn');
      const menu = document.querySelector('.menu');
  
    // Check if the clicked element is the menu button
    if (event.target === menuBtn || menuBtn.contains(event.target)) {
      menuBtn.classList.toggle('open');
      menu.classList.toggle('open');
    }
  });
});    

  
  function addRow(button) {
    // Get the parent table body
    var tbody = button.closest('tbody');

    // Get the current row
    var currentRow = button.closest('tr');

    // Clone the current row
    var newRow = currentRow.cloneNode(true); // true indicates deep cloning  

    // Insert the new row below the current row
    tbody.insertBefore(newRow, currentRow.nextSibling);

    // Add a minus button to the new row if it's not the first row
    if (!currentRow.querySelector('.remove-time')) {
        var minusButton = document.createElement('button');
        minusButton.type = 'button';
        minusButton.className = 'remove-time';
        minusButton.textContent = '-';
        minusButton.onclick = function() {
            removeRow(this);
        };
        newRow.querySelector('td:last-child').appendChild(minusButton);
    }
  }

  function removeRow(button) {
    // Get the parent table body
    var tbody = button.closest('tbody');

    // Get the current row
    var currentRow = button.closest('tr');

    // Remove the current row
    tbody.removeChild(currentRow);
  }
  
  function loadContent(menuOption) {

    document.getElementById('default-content').style.display = 'none';
    
    fetch(`/dashboard/${menuOption}`)
      .then(response => response.text())
      .then(html => {
        // Replace the content of the sub-menu
        document.querySelector('.container').innerHTML = html;
      })
      .catch(error => console.error('Error loading content:', error));
  } 

  function validateForm() {
    var password = document.getElementById("password").value;
    var password_match = document.getElementById("password_match").value;

    if (password !== password_match) {
        alert("Passwords do not match");
        return false; // Prevent form submission
    }
    return true; // Allow form submission
  }

  function formatPhoneNumber() {
    var phoneNumber = document.getElementById("phone_number").value;
    
    // Remove all non-numeric characters
    var formattedPhoneNumber = phoneNumber.replace(/\D/g, '');

    // Apply the desired formatting
    if (formattedPhoneNumber.length >= 3 && formattedPhoneNumber.length <= 6) {
        formattedPhoneNumber = formattedPhoneNumber.slice(0, 3) + '-' + formattedPhoneNumber.slice(3);
    } else if (formattedPhoneNumber.length >= 7) {
        formattedPhoneNumber = formattedPhoneNumber.slice(0, 3) + '-' + formattedPhoneNumber.slice(3, 6) + '-' + formattedPhoneNumber.slice(6);
    }

    // Update the input field value
    document.getElementById("phone_number").value = formattedPhoneNumber;
  }

  // Attach event listener to the phone number input field
  document.getElementById("phone_number").addEventListener("input", formatPhoneNumber);