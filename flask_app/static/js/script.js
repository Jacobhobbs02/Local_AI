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


document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("chat-form");
    const loading = document.getElementById("loading");

    form.addEventListener("submit", function() {
        loading.style.display = "block"
    });
});