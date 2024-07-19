form.onsubmit = function(event) {
    event.preventDefault();
    
    var formData = new FormData(form);
    
    var privileges = [];
    var roles = [];
    
    document.querySelectorAll('input[name="privileges"]:checked').forEach(function(checkbox) {
        privileges.push(checkbox.value);
    });
    
    document.querySelectorAll('input[name="roles"]:checked').forEach(function(checkbox) {
        roles.push(checkbox.value);
    });
    
    formData.append('privileges', JSON.stringify(privileges));
    formData.append('roles', JSON.stringify(roles));

    fetch('/create_user', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        // Check if the response is valid JSON
        return response.text().then(text => {
            try {
                return JSON.parse(text);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                throw new Error('Response is not valid JSON');
            }
        });
    })
    .then(data => {
        createUserMessage.innerHTML = `<p>${data.message}</p>`;
        if (data.status === 'success') {
            createUserMessage.classList.add('success');
            createUserMessage.classList.remove('error');
        } else {
            createUserMessage.classList.add('error');
            createUserMessage.classList.remove('success');
        }
    })
    .catch(error => {
        console.error('Error creating user:', error);
        createUserMessage.innerHTML = `<p>Error creating user. Please try again.</p>`;
        createUserMessage.classList.add('error');
        createUserMessage.classList.remove('success');
    });
}
