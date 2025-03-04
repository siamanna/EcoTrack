function addAction(event) {
    event.preventDefault();
    const actionInput = document.getElementById("sustainable-action").value.trim();
    const actionList = document.getElementById("journal-entries");

    if (actionInput) {
        const listItem = document.createElement("li");
        listItem.textContent = actionInput;
        actionList.appendChild(listItem);

        document.getElementById("sustainable-action").value = ""; // Clear input
    }
}