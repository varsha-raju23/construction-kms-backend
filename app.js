const API_BASE = "https://construction-kms-backend.onrender.com";
async function uploadDocument() {

    const formData = new FormData();

    formData.append(
        "title",
        document.getElementById("title").value
    );

    formData.append(
        "description",
        document.getElementById("description").value
    );

    formData.append(
        "project_name",
        document.getElementById("project_name").value
    );

    formData.append(
        "tags",
        document.getElementById("tags").value
    );

    formData.append(
        "category",
        document.getElementById("category").value
    );

    formData.append(
        "file",
        document.getElementById("file").files[0]
    );

    const response = await fetch(
        `${API_BASE}/api/upload/document`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    document.getElementById(
        "uploadResult"
    ).innerHTML =
        JSON.stringify(data, null, 2);
}


async function searchDocuments() {

    const keyword =
        document.getElementById(
            "keyword"
        ).value;

    const response =
        await fetch(
            `${API_BASE}/api/search/documents?keyword=${keyword}`
        );

    const data =
        await response.json();

    document.getElementById(
        "searchResults"
    ).innerHTML =
        `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}


async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value;

    const response =
        await fetch(
            `${API_BASE}/api/chat/ask`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            }
        );

    const data =
        await response.json();

    document.getElementById("chatResult").innerHTML =
        `<pre>${data.answer || data.error}</pre>`;
}
