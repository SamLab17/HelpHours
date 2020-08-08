// How often we check if the queue is open
var UPDATE_INTERVAL_SECONDS = 15;

checkQueueIsOpen();
setInterval(checkQueueIsOpen, UPDATE_INTERVAL_SECONDS * 1000);

function checkQueueIsOpen() {
    fetch('/queue_status').then(response => response.json())
        .then((data) => {
            if(data && data.status === "OPEN")
                queueIsOpen();
            else
                queueIsClosed(); 
        })
        .catch(queueIsClosed)
}

// If the queue is closed we visually disable the submit button,
// queue status is still checked on the back-end since this the
// 'disabled' attribute can be removed
function queueIsClosed() {
    const joinButton = document.getElementById('submit-button');
    joinButton.disabled = true;
    joinButton.title = 'The queue is closed.';
}

function queueIsOpen() {
    const joinButton = document.getElementById('submit-button');
    joinButton.disabled = false;
    joinButton.removeAttribute('title');
}