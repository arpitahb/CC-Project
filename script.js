async function shortURL() {
    const urlInput = document.getElementById("url").value;
    const resultDiv = document.getElementById("result");

    try {
        const response = await fetch("/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: urlInput }),
        });

        if (response.ok) {
            const data = await response.json();
            resultDiv.innerHTML = `<p>Shortened URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a></p>`;
        } else {
            resultDiv.innerHTML = "<p>Failed to shorten URL. Please try again.</p>";
        }
    } catch (error) {
        console.error("An error occurred:", error);
    }
}
