const apiUrl = document.getElementById('apiurlnew2');

function toggleSelectBox() {
    const box_delete = document.getElementById('box-delete');
    const box_toggle = document.getElementById('box-toggle');
    const box_deleteP = box_toggle.querySelector('p');
    const box_label = document.getElementById('tBoxHead');
    const check_box = document.getElementsByClassName('cheack-box');

    box_label.classList.toggle('hidden');
    box_delete.classList.toggle('hidden');

    if (box_deleteP.textContent === "Multiple Delete") {
        box_deleteP.textContent = "Cancel Delete";
    } else {
        box_deleteP.textContent = "Multiple Delete";
    }

    const length = check_box.length;
    for (let i = 0; i < length; i++) {
        check_box[i].firstElementChild.checked = false;
        check_box[i].classList.toggle('hidden');
    }
}

function deleteSelectedItems() {
    const tBody = document.getElementById('table-body');
    const checked = tBody.querySelectorAll('.select-item:checked');
    let delList = [];

    // Collect selected item IDs
    checked.forEach(checkbox => {
        const row = checkbox.parentElement.parentElement;
        const Id = row.id;
        delList.push(Id);
    });

    toggleSelectBox(); // Hide the delete selection UI

    // Send the delete request and handle redirect
    delRequest(apiUrl.value, delList);
}

function delRequest(url, itemIds) {
    if (!Array.isArray(itemIds) || itemIds.length === 0) {
        console.error("Item IDs should be a non-empty array.");
        return;
    }

    // Prepare the options for the fetch request
    const options = {
        method: "POST", // Use the method your Flask endpoint expects
        headers: {
            "Content-Type": "application/json"
        },
        redirect: "manual", // Handle redirects manually
        body: JSON.stringify({ itemIds }) // Send the item IDs as JSON in the request body
    };

    // Make the fetch request
    fetch(url, options)
        .then(response => {
            if (response.type === "opaqueredirect" || response.status === 0) {
                // Redirect based on the response if it is an opaque redirect or we receive a status 0
                window.location.href = url; // Set the page location to the new URL
            } else if (response.status >= 300 && response.status < 400) {
                // Handle manual redirects by changing the page URL to the value of the "Location" header
                const redirectUrl = response.headers.get('Location');
                if (redirectUrl) {
                    window.location.href = redirectUrl; // Redirect to the new URL
                }
            } else if (!response.ok) {
                throw new Error("Network response was not ok: " + response.statusText);
            }
        })
        .catch(error => {
            console.error("Error occurred during the request:", error); // Handle any errors
        });
}

