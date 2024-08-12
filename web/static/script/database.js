const apiUrl = document.getElementById('apiurlnew');
const url = document.getElementById('url').textContent;
const pass = document.getElementById('pass').textContent;
const user = document.getElementById('user').textContent;
const type = document.getElementById('type').textContent;
const dbname = document.getElementById('dbname').textContent;
// script.js
document.addEventListener("DOMContentLoaded", function() {
    const terminal = document.getElementById('terminal');
    //const inputField = document.createElement('input');
    const inputField = document.getElementById('inputField');
    const beforeInput = document.getElementById('before-input');
    //terminal.appendChild(inputField);

    inputField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const userQuery = inputField.value;
            if (userQuery) {
                displayOutput(`> ${userQuery}`);
                sendQuery(userQuery);
                inputField.value = '';
            }
        }
    });

    function displayOutput(output) {
        const outputElement = document.createElement('div');
        outputElement.textContent = output;
        terminal.insertBefore(outputElement, beforeInput);
        terminal.scrollTop = terminal.scrollHeight;
    }

    function sendQuery(query) {
        // Replace with your actual API call to the remote database
        fetch(`${apiUrl.value}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, url, dbname,  pass, user, type }),
        })
        .then(response => response.json())
        .then(data => {
            displayOutput(data.result);
        })
        .catch(error => {
            displayOutput('Error: ' + error.message);
        });
    }

    inputField.focus();
});


