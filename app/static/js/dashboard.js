document.addEventListener('DOMContentLoaded', function () {
  // Event listener for the menu button
  document.querySelector('.menu-btn').addEventListener('click', function() {
      const menuBtn = document.querySelector('.menu-btn');
      const menu = document.querySelector('.menu');

      menuBtn.classList.toggle('open');
      menu.classList.toggle('open');
  });

  var addBtnCheckInterval = setInterval(function() {
  var addBtn = document.getElementById('add-btn');
  if (addBtn !== null) {
      clearInterval(addBtnCheckInterval); // Stop checking
      addBtn.addEventListener('click', function() {
      var serviceName = document.getElementById('service-name').value;
      var serviceType = document.querySelector('input[name="service-type"]:checked');
      var amount = document.getElementById('amount').value;

      if (!serviceName || !serviceType || !amount) {
          alert("Please fill in all fields.");
          return;
      }

      var serviceTypeValue = serviceType.value;
      var result = serviceName + ": " + serviceTypeValue + " - $" + amount;

      var serviceListInput = document.getElementById('service-list');
      serviceListInput.value +='\n' + result + '\n';
    });
  }
}, 100);

var addEmpCheckInterval = setInterval(function() {
  var addEmp = document.getElementById('add-emp');
  if (addEmp !== null) {
      clearInterval(addEmpCheckInterval); // Stop checking
      addEmp.addEventListener('click', function() {
      var email = document.getElementById('email').value;
      var phoneNumber = document.getElementById('phone_number').value;
      var password = document.getElementById('password').value;
      var firstName = document.getElementById('first-name').value;
      var lastName = document.getElementById('last-name').value;

      if (!email || !phoneNumber || !password || !firstName || !lastName) {
          alert("Please fill in all fields.");
          return;
      }

      var result = firstName + ", " + lastName;
      var hiddenVals = email + ", " + phoneNumber + ', ' + password;
      //var sendPostEmployeeList = result + ', ' + hiddenVals;
      var employeeListInput = document.getElementById('employee-list');
      employeeListInput.value += result;
      var hiddenEmployeeListInput = document.getElementById('hidden-employee-list');
      hiddenEmployeeListInput.value += '\n' + hiddenVals + '\n';
    });
  }
}, 100);
});
  
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
  function updateCalendar(direction, month, year) {

    // Send a GET request to update the calendar
    fetch(`/dashboard/calendar/update_calendar?month=${month}&year=${year}&direction=${direction}`)
      .then(response => response.text())
      .then(html => {
        // Replace the content of the calendar container
        document.querySelector('.container').innerHTML = html;
      })
      .catch(error => console.error('Error updating calendar:', error));
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


    // Define the formatPhoneNumber function
    function formatPhoneNumber(phoneNumberInput) {
            var phoneNumber = phoneNumberInput.value;
            
            // Remove all non-numeric characters
            var formattedPhoneNumber = phoneNumber.replace(/\D/g, '');

            // Apply the desired formatting
            if (formattedPhoneNumber.length >= 3 && formattedPhoneNumber.length <= 6) {
                formattedPhoneNumber = formattedPhoneNumber.slice(0, 3) + '-' + formattedPhoneNumber.slice(3);
            } else if (formattedPhoneNumber.length >= 7) {
                formattedPhoneNumber = formattedPhoneNumber.slice(0, 3) + '-' + formattedPhoneNumber.slice(3, 6) + '-' + formattedPhoneNumber.slice(6);
            }

            // Update the input field value
            phoneNumberInput.value = formattedPhoneNumber;
        }

  function checkPhoneNumberInput() {
    var phoneNumberInput = document.getElementById("phone_number");
    if (phoneNumberInput !== null) {
        formatPhoneNumber(phoneNumberInput); // Format phone number if field exists
    }
  }
  
  // Set interval to continuously check for phone number input field
  var phoneNumberCheckInterval = setInterval(checkPhoneNumberInput, 100);

  // Get all anchor elements within the top navigation
  function loadSubMenu(menuChoice) {
    
    fetch(`/dashboard/admin_center/${menuChoice}`)
      .then(response => response.text())
      .then(html => {
        // Replace the content of the sub-menu
        document.querySelector('.admin-container').innerHTML = html;
      })
      .catch(error => console.error('Error loading content:', error));
  }

  function toggleDropdown(event) {
    event.preventDefault();
    var dropdownContent = document.getElementById("employee-dropdown");
    dropdownContent.style.display = (dropdownContent.style.display === "block") ? "none" : "block";
  }
  function selectEmployee(event) {
    var selectedName = event.target.textContent;
    var selectedId = event.target.getAttribute("data-id");
    document.getElementById("owner-dropdown-btn").textContent = selectedName;
    // Optionally, you can perform additional actions here
    updateCalendar(selectedId);
  }
  function updateCalendar(selectedId) {

    // Send a GET request to update the calendar
    fetch(`/dashboard/availability/update_availability?id=${selectedId}`)
      .then(response => response.text())
      .then(html => {
        // Replace the content of the calendar container
        document.querySelector('.container').innerHTML = html;
      })
      .catch(error => console.error('Error updating calendar:', error));
  } 


