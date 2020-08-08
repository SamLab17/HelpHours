var UPDATE_INTERVAL_SECONDS = 5;

updateQueue();
setInterval(updateQueue, UPDATE_INTERVAL_SECONDS * 1000);


function updateQueue() {
    fetch('/queue').then(response => response.json())
        .then(renderQueue)
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
        output = '<p style="text-align: center;"> The queue is empty. </p>';
    }
    else {
        for (var i = 0; i < queue.length; i++) {
            output += '<div class="queue-entry">';
            output += '<div class="queue-entry-left">';
            output += '<div class="queue-entry-position">' + queue[i].position + '</div>';
            output += '<div class="queue-entry-name">' + queue[i].name + '</div>';
            output += '</div>';
            if("id" in queue[i]){
                output += '<div class="queue-entry-right"><form method="POST" class="queue-entry-buttons">';
                output += '<button name="finished" value=' + queue[i].id + '>Helped</button>';
                output += '<button name="removed" value=' + queue[i].id + '>Remove</button>';
                output += '</form></div>';
            }
            output += '</div>';
        }
    }
    displayQueue(output);
}

function displayQueue(content) {
    document.getElementById('queue').innerHTML = content;
}