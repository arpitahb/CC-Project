async function shortURL() {
  // const BACKEND_URL='https://pq5mudsu43.execute-api.ap-south-1.amazonaws.com/dev'
  // const BACKEND_URL='http://127.0.0.1:8000'

  const AWS_STAGE='dev'
  
  const currentUrl = `${window.location.protocol}/${window.location.host}/${AWS_STAGE}`;
  const urlInput = document.getElementById("url").value;
  const resultDiv = document.getElementById("result");

  try {
    const response = await fetch(`/dev/generate/shorten`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: urlInput }),
    });

    // console.log(await response.json());
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      resultDiv.innerHTML = `<p class="short_url" >Shortened URL: <a href="/${AWS_STAGE}/li/${data.short_url}" target="_blank">${currentUrl}/li/${data.short_url}</a></p>`;
    } else {
      resultDiv.innerHTML = "<p>Failed to shorten URL. Please try again.</p>";
    }
  } catch (error) {
    console.error("An error occurred:", error);
  }
}
