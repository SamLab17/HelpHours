var UPDATE_INTERVAL_SECONDS = 5;

updateQueue();
setInterval(updateQueue, UPDATE_INTERVAL_SECONDS * 1000);


function updateQueue() {
    fetch('/queue').then(response => renderQueue(response.json()))
        .catch(() => {
            displayQueue(
                '<p style="text-align: center;"> Couldn\'t connect to the server to retrieve the queue. </p>'
            )
        });
}

function renderQueue(data) {
    var output = '';
    var queue = data.queue;
    if (!queue || queue.length === 0) {
        output = '<p style="text-align: center;"> The Queue is empty. </p>';
    }
    else {
        for (var i = 0; i < queue.length; i++) {
            output += '<div class="queue-entry"><div class="queue-entry-left"><div class="queue-entry-position">';
            output += queue[i].position;
            output += '</div><div class="queue-entry-name">';
            output += queue[i].name;
            output += '</div></div></div>';
        }
    }
    displayQueue(output);
}

function displayQueue(content) {
    document.getElementById('queue').innerHTML = content;
}