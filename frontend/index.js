
document.getElementById("file-upload").onchange = function(){
    document.querySelector("#file-name").textContent = this.files[0].name;
  }

 // Get references to the DOM elements
const fileUpload = document.getElementById('file-upload');
const fileName = document.getElementById('file-name');
const form = document.querySelector('.home-form');
const submitButton = form.querySelector('button');

// Update the file name when a file is chosen
fileUpload.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    fileName.textContent = `Selected file: ${file.name}`;
  } else {
    fileName.textContent = '';
  }
});

// Add a submit event listener to the form
form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the default form submission

  // Create a new FormData object
  const formData = new FormData();

  // Append the file to the FormData object
  const file = fileUpload.files[0];
  if (file) {
    console.log("appended!!!!!!!");
    formData.append('file', file);
  }

  // Use Fetch API to send the form data to the server
  fetch('/submit', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.text())
    .then(data => {
      console.log(data); // Handle the response from the server
      alert('File uploaded successfully!'); // Show success message to user
    })
    .catch(error => {
      console.error('Error:', error); // Handle any errors
    });
});
