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