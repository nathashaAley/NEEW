$(document).ready(function() {
    $('#long-running-queries-form').submit(function(event) {
        event.preventDefault();  // Prevent default form submission

        var elapsedTime = $('#long-running-queries-input').val();

        // Send AJAX request to Flask endpoint
        $.ajax({
            url: '/fetch-long-running-queries',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ elapsed_time: elapsedTime }),
            success: function(response) {
                if (response.success) {
                    displayQueries(response.queries);
                } else {
                    console.error('Error fetching long-running queries:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    function displayQueries(queries) {
        var outputDiv = $('#long-running-queries-output');
        outputDiv.empty();  // Clear previous results

        queries.forEach(function(query) {
            var queryHtml = `
                <div class="query-item">
                    <p><strong>SQL ID:</strong> ${query.sql_id}</p>
                    <p><strong>SQL Text:</strong> ${query.sql_text}</p>
                    <p><strong>Start Time:</strong> ${query.start_time}</p>
                    <p><strong>Last Active Time:</strong> ${query.last_active_time}</p>
                    <p><strong>Elapsed Time (sec):</strong> ${query.elapsed_sec}</p>
                    <hr>
                </div>
            `;
            outputDiv.append(queryHtml);
        });
    }
});
