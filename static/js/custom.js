//async function submit() {
 //   const response = await fetch('/submit');
  //  const data = await response.json();
  //  var newDiv = document.createElement("div");
  //  newDiv.innerHTML = "ha ha" //data.message;
  //  document.body.appendChild(newDiv);
// }

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('stringForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        fetch('/submit', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('responseMessage').innerText = data.message;
        })
        .catch(error => console.error('Error:', error));
    });

    // Periodic polling
    setInterval(() => {
        fetch('/poll')
            .then(response => response.json())
            .then(data => {
                document.getElementById('pollResult').innerText = 'Server: ' + data.current_time;
            })
            .catch(error => console.error('Error:', error));
    }, 5000); // Poll every 5000 milliseconds (5 seconds)
});

