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
		box_deleteP.textContent = "Cancel Delete"
	} else {
		box_deleteP.textContent = "Multiple Delete"
	}

	const length = check_box.length;
	for (let i=0; i < length; i++) {
		check_box[i].firstElementChild.checked = false;
		check_box[i].classList.toggle('hidden');
	}
}

function deleteSelectedItems() {
	const tBody = document.getElementById('table-body');
	const checked = tBody.querySelectorAll('.select-item:checked')
	let delList = []
	checked.forEach(checkbox => {
                const row = checkbox.parentElement.parentElement
		const Id = row.id
		delList.push(Id)
                tBody.removeChild(row);
            });
	toggleSelectBox();
	let Url = `${apiUrl.value}`
	delRequest(Url, delList)
		.then(response => {
			console.log("Response from API:", response);
		})
		.catch(error => {
			console.error("Error occurred:", error);
		});
}

function delRequest(url, itemIds, headers = {}) {
  if (!Array.isArray(itemIds) || itemIds.length === 0) {
    throw new Error("Item IDs should be a non-empty array.");
  }

  // Prepare the options for the fetch request
  const options = {
    method: "DELETE", // HTTP DELETE method
    headers: {
      "Content-Type": "application/json", // Ensure JSON content type
      ...headers // Add any additional headers provided
    },
    redirect: "follow", // Automatically follow redirects
    body: JSON.stringify({ itemIds }) // Send the item IDs as JSON in the request body
  };

  // Make the fetch request without awaiting the response
  fetch(url, options)
    .catch(error => {
      console.error("Error sending delete request:", error); // Handle any errors
    });
}


function deilRequest(url, itemIds, headers = {}) {
  if (!Array.isArray(itemIds) || itemIds.length === 0) {
    throw new Error("Item IDs should be a non-empty array.");
  }

  // Prepare the options for the fetch request
  const options = {
    method: "DELETE", // HTTP DELETE method
    headers: {
      "Content-Type": "application/json", // Ensure JSON content type
      ...headers // Add any additional headers provided
    },
    redirect: "follow", // Handle redirects manually
    body: JSON.stringify({ itemIds }) // Send the item IDs as JSON in the request body
  };

  // Make the fetch request
  return fetch(url, options)
    .then(response => {
      // Check if the response is a redirect (3xx status code)
      if (response.status >= 300 && response.status < 400) {
        const redirectUrl = response.headers.get('Location');
        if (redirectUrl) {
          // Perform the redirect by changing the window location
          window.location.href = redirectUrl;
          return; // Exit the function after redirecting
        }
      }

      // Handle non-redirect responses
      if (!response.ok) {
        throw new Error("Network response was not ok: " + response.statusText);
      }
      return response.json(); // Parse the response as JSON
    })
    .then(data => {
      if (data) {
        console.log("Items deleted successfully:", data); // Handle the success response
        return data; // Return the response data to the caller
      }
    })
    .catch(error => {
      console.error("Error deleting items:", error); // Handle any errors
      throw error; // Re-throw the error for further handling
    });
}

