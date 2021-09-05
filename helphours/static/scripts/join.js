// How often we check if the queue is open
const UPDATE_INTERVAL_SECONDS = 10;

checkQueueIsOpen();
setInterval(checkQueueIsOpen, UPDATE_INTERVAL_SECONDS * 1000);

function checkQueueIsOpen() {
    fetch('/queue_status').then(response => response.json())
        .then((data) => {
            // Since we have two queues now, this gets a bit weirder.
            // We'll leave the join button enabled if either queue is open.
            // This means a join request may fail if the "wrong" queue
            // was open, but the backend handles this and an error
            // will be displayed.
            if(data && (data.virtual_open || data.in_person_open))
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
