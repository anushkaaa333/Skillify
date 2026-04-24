// Tiny script for universal interactions

document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Loading Effect for Form Submissions
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function() {
            const btn = this.querySelector('button[type="submit"]');
            if (btn) {
                btn.innerText = "Processing...";
                btn.classList.add("processing");
            }
        });
    });

    // 2. Play Toast stored from previous page
    const toastMessage = sessionStorage.getItem("toastMessage");
    if (toastMessage) {
        showToast(toastMessage);
        sessionStorage.removeItem("toastMessage");
    }

    // 3. Simple click-grab for Logout
    const logoutBtn = document.querySelector('a[href="/logout"]');
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            sessionStorage.setItem("toastMessage", "Logged out successfully!");
        });
    }
});

// Helper: Visual Toast Notification (No complex logic)
function showToast(message) {
    let container = document.querySelector(".toast-container");
    if (!container) {
        container = document.createElement("div");
        container.className = "toast-container";
        document.body.appendChild(container);
    }
    
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerText = message;
    
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
