// Added By: Urvashi Kohale
async function createPost(event) {
    event.preventDefault();

    const content = document.getElementById("status").value;
    if (!content) {
        alert("Enter a status update.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/post", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content }),
        });
        console.log("Response:", response);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        document.getElementById("postDisplay").style.display = "inline-block";

        document.getElementById("postDisplay").innerHTML = `
            <strong>Post Created:</strong> ${data.content} <br>
            <strong>ID:</strong> ${data.id}
        `;

        await loadPostIds();
    } catch (error) {
        console.error("Error creating post:", error);
        alert("Failed to create the post.");
    }
}

// Added by: Uravshi Kohale
async function loadPostIds() {
    try {
        const response = await fetch("http://127.0.0.1:8000/post_ids");
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        const dropdown = document.getElementById("postIdDropdown");
        dropdown.innerHTML = "";  

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Select Post ID";
        dropdown.appendChild(defaultOption);

        if (!data.ids || data.ids.length === 0) {
            console.log("No post IDs available.");
            return;
        }

        data.ids.forEach(id => {
            const option = document.createElement("option");
            option.value = id;
            option.textContent = id;
            dropdown.appendChild(option);
        });

    } catch (error) {
        alert("Please connect to the server and reload the page.");
    }
}

// Added by: Indraneel Sarode
async function getPost() {
    const id = document.getElementById("postIdDropdown").value;
    if (!id) {
        alert("Select a post ID.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/post/${id}`);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        const createdDate = new Date(data.created_at);
        const date = createdDate.toLocaleDateString();
        const time = createdDate.toLocaleTimeString();

        document.getElementById("postDisplay").innerHTML = `
            <strong>Date:</strong> ${date} <br>
            <strong>Time:</strong> ${time} <br>
            <strong>Post:</strong> ${data.content}
        `;
        document.getElementById("postDisplay").style.display = "inline-block";
    } catch (error) {
        console.error("Error fetching post:", error);
        alert("Failed to retrieve the post. Check the console for details.");
    }
}

// Added by: Indraneel Sarode
async function deletePost(event) {
    event.preventDefault(); 

    const id = document.getElementById("postIdDropdown").value;
    if (!id) {
        alert("Select a post ID.");
        return;
    }

    if (!confirm("Are you sure you want to delete this post?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/post/${id}`, { 
            method: "DELETE" 
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        document.getElementById("postDisplay").innerHTML = `<strong>Post Deleted.</strong>`;
        document.getElementById("postDisplay").style.display = "inline-block";

        await loadPostIds();
    } catch (error) {
        console.error("Error deleting post:", error);
        alert("Failed to delete the post.");
    }
}


try {
    window.onload = loadPostIds;
} catch (error) {
    alert("Please connect to the server and reload the page.");
}
