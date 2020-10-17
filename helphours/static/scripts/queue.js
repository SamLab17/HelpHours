// How many seconds we should wait before polling the server again
const UPDATE_INTERVAL_SECONDS = 10;

// After 120 minutes of not refreshing the page or clicking any buttons
// stop making requests to the API
const TIMEOUT_MINUTES = 120;

// Hold previous fetch result, if it's the same, don't bother re-rendering
var lastPullResponse;

// Fetch the queue when the page loads
updateQueue();

var updateInterval = setInterval(updateQueue, UPDATE_INTERVAL_SECONDS * 1000);

setTimeout(() => {
    clearInterval(updateInterval);
    clearQueue();
    displayMessage('Connection timed out, refresh the page.')
}, TIMEOUT_MINUTES * 60 * 1000);


function updateQueue() {
    fetch('/queue').then(response => response.json())
        .then(renderQueue)
        .catch((e) => {
            clearQueue();
            displayMessage('Couldn\'t connect to the server to retrieve the queue.');
            console.log(e);
        });
}

function renderQueue(data) {
    let dataJSON = JSON.stringify(data);
    if(lastPullResponse === dataJSON){
        // Nothing changed, don't bother re-rendering
        return;
    }

    // Queue changed, let's re-render and save this result
    clearQueue();
    lastPullResponse = dataJSON;

    let queue = data.queue;

    if (!queue || queue.length === 0) {
        displayMessage('The queue is empty.');
    }
    else {
        let queueContainer = document.getElementById("queue");
        let template = document.getElementById("queue-entry-template");
        for (let i = 0; i < queue.length; i++) {
            let newEntry = template.content.cloneNode(true);
            newEntry.querySelector('.queue-entry-position').textContent = queue[i].position;
            newEntry.querySelector('.queue-entry-name').textContent = queue[i].name;

            if("id" in queue[i]){
                newEntry.querySelectorAll('button').forEach(button => 
                    button.value=queue[i].id
                );
            } else {
                // Hide "Help" and "Remove" buttons
                newEntry.querySelectorAll('button').forEach(button =>
                    button.style.display = 'none'
                );
            }
            queueContainer.appendChild(newEntry);
        }
    }
}

function clearQueue() {
   let queue = document.getElementById("queue");
   if(queue)
        while(queue.firstChild)
            queue.removeChild(queue.firstChild)
}

function displayMessage(content) {
    let message = document.getElementById('queue-message').content.cloneNode(true);
    message.querySelector('.queue-message').textContent = content;
    document.getElementById('queue').appendChild(message);
}
