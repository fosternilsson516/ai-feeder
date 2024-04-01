document.addEventListener('DOMContentLoaded', function () {
  // Event listener for the menu button
  document.querySelector('.menu-btn').addEventListener('click', function() {
      const menuBtn = document.querySelector('.menu-btn');
      const menu = document.querySelector('.menu');

      menuBtn.classList.toggle('open');
      menu.classList.toggle('open');
  });
});
  
  function loadContent(menuOption) {
    fetch(`/dashboard/${menuOption}`)
      .then(response => response.text())
      .then(html => {
        // Replace the content of the sub-menu
        document.querySelector('.container').innerHTML = html;
        if (menuOption === 'setup_chat') {
          initializeSetupChat();
        }
      })
      .catch(error => console.error('Error loading content:', error));
  }
  function initializeSetupChat() {
    scrollToBottom();
    const textarea = document.querySelector('textarea[name="answer"]');

    if (textarea) {
        textarea.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey && !event.ctrlKey) {
                event.preventDefault();
                const { selectionStart, selectionEnd } = textarea;
                textarea.value = textarea.value.substring(0, selectionStart) + "\n" + textarea.value.substring(selectionEnd);
                textarea.setSelectionRange(selectionStart + 1, selectionStart + 1);
                autoResize(textarea); // Pass textarea as argument
            }
        });

        textarea.addEventListener('input', () => autoResize(textarea)); // Pass textarea as argument
    }

    // Copy answer to textarea on double-click
    document.querySelectorAll('.chat-message').forEach(element => {
        element.addEventListener('dblclick', function() {
            copyAnswerToTextarea(element, textarea); // Pass textarea as argument
        });
    });
}
function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}
function copyAnswerToTextarea(chatMessageElement, textarea) {
  const questionId = chatMessageElement.getAttribute('data-question-id');
  const answerText = chatMessageElement.querySelector('.preformatted').textContent.trim();
  const questionIdInput = document.querySelector('input[name="question_id"]');

  if (textarea && questionIdInput) {
      textarea.value = answerText;
      questionIdInput.value = questionId;
      autoResize(textarea); // Use the passed textarea
      textarea.focus();
      textarea.setSelectionRange(textarea.value.length, textarea.value.length);
  }
}
function scrollToBottom() {
  const chatMessages = document.getElementById('messages');
  if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}
function displayMessage(message, type) {
  const messageAlertDiv = document.getElementById('message-alert');
  messageAlertDiv.textContent = message; // Sets the text of the message
  messageAlertDiv.className = 'alert'; // Apply the base alert class
  messageAlertDiv.classList.add(type); // Adds a class for styling based on the message type ('error', 'success', etc.)
  messageAlertDiv.style.display = 'block'; // Make the message alert visible
}
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('.container').addEventListener('submit', function(e) {
    if (e.target && e.target.id === 'myForm') {
      e.preventDefault();
       
      console.log('Form submission prevented. JS is handling submission.');
      const form = e.target;
      const formData = new FormData(form);
      fetch(form.action, {
          method: 'POST',
          body: formData,
      })
      
      .then(response => {
          if (response.status === 204) {
              // Assuming 'menuOption' is known or stored globally
              loadContent('setup_chat'); 
          } else if (response.status === 409) {
            return response.json().then(data => {
              displayMessage(data.message, "error");
          });    
          } else {
              console.error('Server error');
              // Handle server error (e.g., show error message)
              displayMessage("An unexpected error occurred. Please try again.", "error");
          }
      })
      .catch(error => {
        console.error('Error:', error);
        displayMessage("A network error occurred. Please check your connection and try again.", "error");
    });
  }
});
});



 



