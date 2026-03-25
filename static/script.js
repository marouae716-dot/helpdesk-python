document.addEventListener("DOMContentLoaded", function () {
    const sections = [
        { headerId: "tickets-header", contentId: "tickets-content", arrowId: "tickets-arrow" },
        { headerId: "queue-header", contentId: "queue-content", arrowId: "queue-arrow" },
        { headerId: "history-header", contentId: "history-content", arrowId: "history-arrow" }
    ];

    sections.forEach(s => {
        const header = document.getElementById(s.headerId);
        const content = document.getElementById(s.contentId);
        const arrow = document.getElementById(s.arrowId);
        if (header && content && arrow) {
            header.addEventListener("click", function () {
                if (content.classList.contains("hidden")) {
                    content.classList.remove("hidden");
                    arrow.textContent = "▲";
                } else {
                    content.classList.add("hidden");
                    arrow.textContent = "▼";
                }
            });
        }
    });

    const searchInput = document.getElementById("search-input");
    const ticketsList = document.getElementById("tickets-list");

    if (searchInput && ticketsList) {
        searchInput.addEventListener("input", function () {
            const term = searchInput.value.toLowerCase();
            const items = ticketsList.querySelectorAll("li");
            items.forEach(li => {
                const text = li.textContent.toLowerCase();
                li.style.display = text.includes(term) ? "" : "none";
            });
        });
    }
});
