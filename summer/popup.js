async function extractAndProcessData() {
	const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

	// extract title and text from current webpage
	chrome.scripting.executeScript(
		{
			target: { tabId: tab.id },
			func: () => ({
				title: document.title,
				text: document.body.innerText
			}),
		},
		async (results) => {
			if (results && results[0] && results[0].result) {
				const { title, text } = results[0].result;

				// sent title and text to server
				try {
					const response = await fetch("http://localhost:5000/summer", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({
							title: title.trim(),
							text: text.trim()
						})
					});

					if (response.ok) {
						const data = await response.json();
						document.getElementById("title").innerText = `${data.title}`;
						document.getElementById("tag").innerHTML = `<strong>Tag : </strong>${data.tag}`;
						document.getElementById("summary").innerText = `${data.summary}`;
					} else {
						document.getElementById("title").innerText = "(Internal Server Error)";
					}
				} catch (error) {
					console.error(error);
					document.getElementById("title").innerText = "(Server Unavailable)";
				}
			} else {
				document.getElementById("title").innerText = "(Text Extraction Failed)";
			}
		}
	);
}

// run on popup load
document.addEventListener("DOMContentLoaded", extractAndProcessData);
