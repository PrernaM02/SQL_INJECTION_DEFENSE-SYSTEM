document.addEventListener("DOMContentLoaded", function () {
    let flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(msg => {
        setTimeout(() => msg.style.display = "none", 3000);
    });
});