document.addEventListener('DOMContentLoaded', function() {
    const sessionLockCard = document.getElementById('session-locks-card');
    const sessionLockList = document.getElementById('session-locks-list');

    function fetchSessionLockDetails() {
        fetch('/get_session_locks_data')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                sessionLockList.innerHTML = '';

                if (data.error) {
                    const errorItem = document.createElement('li');
                    errorItem.textContent = data.error;
                    sessionLockList.appendChild(errorItem);
                } else if (data.length === 0) {
                    const noLocksItem = document.createElement('li');
                    noLocksItem.textContent = 'No session locks found';
                    sessionLockList.appendChild(noLocksItem);
                } else {
                    data.forEach(session => {
                        const sessionItem = document.createElement('li');

                        // Create separate <p> elements for each detail
                        const blockingSid = document.createElement('p');
                        blockingSid.textContent = `Blocking SID: ${session.blocking_sid}`;
                        sessionItem.appendChild(blockingSid);

                        const blockedSid = document.createElement('p');
                        blockedSid.textContent = `Blocked SID: ${session.blocked_sid}`;
                        sessionItem.appendChild(blockedSid);

                        const sqlId = document.createElement('p');
                        sqlId.textContent = `SQL ID: ${session.sql_id}`;
                        sessionItem.appendChild(sqlId);

                        const status = document.createElement('p');
                        status.textContent = `Status: ${session.status}`;
                        sessionItem.appendChild(status);

                        const serialNum = document.createElement('p');
                        serialNum.textContent = `Serial#: ${session.serial_num}`;
                        sessionItem.appendChild(serialNum);

                        const sqlFulltext = document.createElement('p');
                        sqlFulltext.textContent = `SQL Text: ${session.sql_fulltext}`;
                        sessionItem.appendChild(sqlFulltext);

                        sessionLockList.appendChild(sessionItem);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching session lock details:', error);
                sessionLockList.innerHTML = ''; // Clear previous content
                const errorItem = document.createElement('li');
                errorItem.textContent = 'Error fetching session lock details';
                sessionLockList.appendChild(errorItem);
            });
    }

    if (sessionLockCard) {
        sessionLockCard.addEventListener('click', fetchSessionLockDetails);
    } else {
        console.warn('session-locks-card not found.');
    }
});
