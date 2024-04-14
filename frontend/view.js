// if the id ask button is clicked get the content from the input field, id que, and send it to the server @app.route('/question/<question>')
var container = document.getElementById('adad');
container.src = "https://9b1d-64-165-34-3.ngrok-free.app/releaseq"

document.getElementById('ask').addEventListener('click', function() {
    var abd = document.getElementById('bad');
    abd.style.visibility = 'hidden';
    var question = document.getElementById('que').value;
    console.log(question);
    fetch('/question/' + document.getElementById('que').value)
        .then((response) => {

            var containert = document.getElementById('adad');
            containert.src = "https://9b1d-64-165-34-3.ngrok-free.app/releaseq"
            document.getElementById("tra").load();
            abd.style.visibility = 'visible';

            // container.src = "https://9b1d-64-165-34-3.ngrok-free.app/releaseq"
        })

});