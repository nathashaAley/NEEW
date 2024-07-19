document.addEventListener('DOMContentLoaded', function() {
    const log4jVulnerabilitiesCard = document.getElementById('log4j-vulnerabilities-card');
    const log4jVulnerabilitiesList = document.getElementById('log4j-vulnerabilities-list');
    const log4jVulnerabilitiesHeading = document.getElementById('log4j-vulnerabilities-heading');

    function fetchLog4jVulnerabilities() {
        fetch('/fetch-log4j-vulnerability')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Clear previous content
                log4jVulnerabilitiesList.innerHTML = '';

                if (data.error) {
                    const errorItem = document.createElement('li');
                    errorItem.textContent = data.error;
                    log4jVulnerabilitiesList.appendChild(errorItem);
                } else {
                    // Create elements for new content
                    const titleHeading = document.createElement('h3');
                    titleHeading.textContent = data.title.trim();
                    const releaseDateItem = document.createElement('p');
                    releaseDateItem.textContent = `Release Date: ${data.release_date}`;
                    const filenameItem = document.createElement('p');
                    filenameItem.textContent = `Filename: ${data.filename}`;

                    // Append new content items
                    log4jVulnerabilitiesList.appendChild(titleHeading);
                    log4jVulnerabilitiesList.appendChild(releaseDateItem);
                    log4jVulnerabilitiesList.appendChild(filenameItem);

                    // Hide the heading if it exists
                    if (log4jVulnerabilitiesHeading) {
                        log4jVulnerabilitiesHeading.style.display = 'none';
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching Log4j vulnerabilities:', error);
                log4jVulnerabilitiesList.innerHTML = ''; // Clear previous content
                const errorItem = document.createElement('li');
                errorItem.textContent = 'Error fetching Log4j vulnerabilities';
                log4jVulnerabilitiesList.appendChild(errorItem);

                // Show the heading if it exists and no content loaded
                if (log4jVulnerabilitiesHeading) {
                    log4jVulnerabilitiesHeading.style.display = 'block';
                }
            });
    }

    if (log4jVulnerabilitiesCard) {
        log4jVulnerabilitiesCard.addEventListener('click', fetchLog4jVulnerabilities);
    } else {
        console.warn('log4j-vulnerabilities-card not found.');
    }
});
