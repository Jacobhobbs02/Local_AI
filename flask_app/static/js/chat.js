/* lets user click enter to send prompts*/
document.addEventListener("DOMContentLoaded", function() {
    const prompt = document.getElementById("prompt");
    const form = document.getElementById("chat-form");

    if (prompt) {
        prompt.addEventListener("input", function() {
            this.style.height = "auto";
            this.style.height = this.scrollHeight + "px";
        });

        prompt.addEventListener("keydown", function(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                e.stopImmediatePropagation();
                form.requestSubmit();
            }
        });
    } 
});

/* helps loading dot preform when page loads */
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("chat-form");
    const loading = document.getElementById("loading");

    form.addEventListener("submit", function() {
        loading.style.display = "block"
    });
});
window.onload = function() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
};


// Chat Context Menu
const menu = document.getElementById("context-menu");

document.querySelectorAll(".extras").forEach(button => {
    button.addEventListener("click", (e) => {
        e.stopPropagation();

        const rect = button.getBoundingClientRect();

        menu.style.left = `${rect.right + 8}px`;
        menu.style.top = `${rect.top}px`;
        menu.style.display = "block";

        menu.dataset.chatId = button.dataset.id;
    });
});


// Profile Context Menu
const profileButton = document.querySelector(".profile");
const profileContextMenu = document.getElementById("context-profile-menu");
const profileMenu = document.getElementById("profile-menu");
const openProfile = document.getElementById("open-profile");

profileButton.addEventListener("click", (e) => {
    e.stopPropagation();

    profileContextMenu.style.display = "block";

    const rect = profileButton.getBoundingClientRect();

    profileContextMenu.style.left = `${rect.right + 8}px`;
    profileContextMenu.style.top = `${rect.top - 60}px`; // Move menu upward
});


// Open the profile modal
openProfile.addEventListener("click", (e) => {
    e.stopPropagation();

    profileContextMenu.style.display = "none";
    profileMenu.style.display = "block";
});


// Close menus when clicking elsewhere
document.addEventListener("click", (e) => {

    // Close chat context menu
    if (
        !menu.contains(e.target) &&
        !e.target.classList.contains("extras")
    ) {
        menu.style.display = "none";
    }

    // Close profile context menu
    if (
        !profileContextMenu.contains(e.target) &&
        !profileButton.contains(e.target)
    ) {
        profileContextMenu.style.display = "none";
    }

    // Close profile modal
    if (
        !profileMenu.contains(e.target) &&
        e.target !== openProfile
    ) {
        profileMenu.style.display = "none";
    }

});




let currentRow = null;

document.querySelectorAll(".extras").forEach(button => {
    button.addEventListener("click", (e) => {
        e.stopPropagation();
        currentRow = button.closest(".group-row");
    });
});

document.getElementById("rename-chat").addEventListener("click", () => {

    if (!currentRow) return;

    const link = currentRow.querySelector(".group-item");
    const form = currentRow.querySelector(".rename-form");
    const input = currentRow.querySelector(".rename-title");

    link.style.display = "none";
    form.style.display = "inline-block";

    input.focus();
    input.select();

    menu.style.display = "none";
});

document.querySelectorAll(".rename-title").forEach(input => {

    // Submit on Enter
    input.addEventListener("keydown", e => {
        if (e.key === "Enter") {
            e.preventDefault();
            input.form.submit();
        }
    });

    // Cancel on click away
    input.addEventListener("blur", () => {
        const row = input.closest(".group-row");

        row.querySelector(".group-item").style.display = "";
        row.querySelector(".rename-form").style.display = "none";
    });

});







// Text to Speech
document.addEventListener("click", function (e) {

    if (!e.target.classList.contains("speak-btn")) return;

    // If already speaking, stop.
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
        return;
    }

    const text = e.target.closest(".ai").querySelector("p").innerText;

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    speechSynthesis.speak(speech);

});