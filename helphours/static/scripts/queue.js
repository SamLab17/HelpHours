const UPDATE_INTERVAL_SECONDS = 5;

// Hold previous fetch result, if it's the same, don't bother re-rendering
var lastPullResponse;

updateQueue();
setInterval(updateQueue, UPDATE_INTERVAL_SECONDS * 1000);


function updateQueue() {
    fetch('/queue').then(response => response.json())
        .then(renderQueue)
        .catch(() => {
            clearQueue();
            displayMessage('Couldn\'t connect to the server to retrieve the queue.')
        });
}

function renderQueue(data) {
    let dataJSON = JSON.stringify(data);
    if(lastPullResponse === dataJSON){
        return;
    } else {
        clearQueue();
        lastPullResponse = dataJSON;
    }


    let queue = data.queue;


    if (!queue || queue.length === 0) {
        displayMessage('The queue is empty.');
    }
    else {
        let queueContainer = document.getElementById("queue");
        let template = document.getElementById("queue-entry-template");
        for (var i = 0; i < queue.length; i++) {
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
