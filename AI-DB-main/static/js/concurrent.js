document.addEventListener('DOMContentLoaded', function() {
    const concurrentProgramsCard = document.getElementById('concurrent-programs-card');
    const concurrentProgramsList = document.getElementById('concurrent-programs-list');

    function fetchConcurrentPrograms() {
        fetch('/fetch-concurrent-programs')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                concurrentProgramsList.innerHTML = '';

                if (data.error) {
                    const errorItem = document.createElement('li');
                    errorItem.textContent = data.error;
                    concurrentProgramsList.appendChild(errorItem);
                } else {
                    data.forEach(program => {
                        const programItem = document.createElement('li');
                        programItem.innerHTML = `
                            <p><strong>Program Name:</strong> ${program.program_name}</p>
                            <p><strong>Status:</strong> ${program.status}</p>
                            <p><strong>Start Time:</strong> ${program.start_time}</p>
                            <p><strong>End Time:</strong> ${program.end_time}</p>
                            <p><strong>Progress:</strong> ${program.progress}</p>
                        `;
                        concurrentProgramsList.appendChild(programItem);
                    });

                    // Add notification dot and number logic here
                    // Example: check for notifications and update UI
                }
            })
            .catch(error => {
                console.error('Error fetching concurrent programs:', error);
                concurrentProgramsList.innerHTML = ''; // Clear previous content
                const errorItem = document.createElement('li');
                errorItem.textContent = 'Error fetching concurrent programs';
                concurrentProgramsList.appendChild(errorItem);
            });
    }

    if (concurrentProgramsCard) {
        fetchConcurrentPrograms();

        // Example: Adding event listeners for management actions (stop, restart, reschedule)
        concurrentProgramsCard.addEventListener('click', function(event) {
            // Handle management actions based on clicked element
            const action = event.target.dataset.action;
            if (action === 'stop') {
                // Implement stop action
            } else if (action === 'restart') {
                // Implement restart action
            } else if (action === 'reschedule') {
                // Implement reschedule action
            }
        });
    } else {
        console.warn('concurrent-programs-card not found.');
    }
});
