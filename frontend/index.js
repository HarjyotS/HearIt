const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

const rep = async () => {
  while (true) {
    await sleep(1000)
    // Wait for 1 second
    console.log("Checking status...")
  
  
    // Do something
    fetch('/status', { 
      method: 'GET'
    })
    .then(function(response) { return response.json(); })
    .then(function(json) {
      console.log(json["status"]);
      if(json["status"] == "Processing"){
        var ud = json["updates"];
        var fsti = ``;
        for (var i = 0; i < ud.length; i++) {
          // Calculate the current time
          var currentTime = Date.now();
          
          // Calculate the time difference in milliseconds
          var timeDifference = currentTime - (ud[i]["time"] * 1000);
          
          // Convert the time difference to seconds
          var timeDifferenceInSeconds = timeDifference / 1000;
          
          // Calculate minutes and seconds from the time difference
          var minutes = Math.floor(timeDifferenceInSeconds / 60);
          var seconds = Math.floor(timeDifferenceInSeconds % 60);
          
          // Format the minutes and seconds as a string
          var timeAgoString = `(${minutes} minutes and ${seconds} seconds ago)`;
          
          // Update the fsti string with the message and time ago
          fsti += `${ud[i]["message"]} ${timeAgoString}<br>`;
        }
        document.getElementById("updates").innerHTML = fsti;
      }
      if(json["status"] == "Complete"){
        window.location.replace("view.html")
      }
      // use the json
    });
  }
}

rep()
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
