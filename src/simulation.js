// Basic UI switching
function showSection(id) {
    document.querySelectorAll("section").forEach(s => s.classList.remove("visible"));
    document.getElementById(id).classList.add("visible");
}

// Placeholder for fetching/updating products
document.getElementById('saveProducts').onclick = () => {
    // TODO: POST /api/products to backend
    alert("Products saved (placeholder).");
};

// Placeholder for simulation trigger
document.getElementById('sellNow').onclick = () => {
    // TODO: POST /api/start-agent
    document.getElementById("status").textContent = "Simulation running...";
};


document.addEventListener('DOMContentLoaded', () => {
    const sellBtn = document.getElementById('sellNow');
    const stopBtn = document.getElementById('stopNow');
    const status = document.getElementById('status');

    if (stopBtn) stopBtn.disabled = true;

    if (sellBtn) {
    sellBtn.addEventListener('click', () => {
        status.textContent = 'Simulation running...';
        sellBtn.disabled = true;
        if (stopBtn) stopBtn.disabled = false;
        // TODO: POST /api/start-agent
    });
    }

    if (stopBtn) {
    stopBtn.addEventListener('click', () => {
        status.textContent = 'Simulation stopped.';
        if (sellBtn) sellBtn.disabled = false;
        stopBtn.disabled = true;
        // TODO: POST /api/stop-agent
    });
    }
});