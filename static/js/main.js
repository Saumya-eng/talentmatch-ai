// ---------------- FILE PREVIEW ---------------- //
document.getElementById("files").addEventListener("change", function () {
    const files = Array.from(this.files);

    if (files.length === 0) {
        document.getElementById("fileNames").innerText = "";
        return;
    }

    const names = files.map(f => `${f.name} (${(f.size / 1024).toFixed(1)} KB)`);

    document.getElementById("fileNames").innerHTML =
        "<b>Uploaded:</b><br>" + names.join("<br>");
});


// ---------------- FORM SUBMIT ---------------- //
const form = document.getElementById("form");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const jd = document.getElementById("jd").value;
    const files = document.getElementById("files").files;

    if (!jd || files.length === 0) {
        alert("Please enter job description and upload resumes");
        return;
    }

    const formData = new FormData();
    formData.append("job_description", jd);

    for (let file of files) {
        formData.append("resumes", file);
    }

    const container = document.getElementById("results");
    container.innerHTML = `<div class="loading">Processing resumes...</div>`;

    const btn = document.querySelector("button");
    btn.disabled = true;
    btn.innerText = "Matching...";

    try {
        const response = await fetch("/match", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!data.success || !data.results) {
            container.innerHTML = `<p class="empty-message">No results returned</p>`;
            alert(data.error || "Something went wrong");
            return;
        }

        // Save globally
        window.lastResults = data.results;

        displayResults(data.results);
        renderCharts(data.results);

    } catch (error) {
        console.error(error);
        container.innerHTML = `<p class="empty-message">Server error occurred</p>`;
        alert("Error connecting to server");
    }

    btn.disabled = false;
    btn.innerText = "Match Resumes";
});


// ---------------- FILTER LOGIC ---------------- //
function getFilteredResults() {
    const minScore = parseFloat(document.getElementById("minScore").value) || 0;
    const skillFilter = document.getElementById("skillFilter").value.toLowerCase().trim();

    return window.lastResults.filter(r => {
        if (r.final_score < minScore) return false;
        if (skillFilter && !r.skills.some(s => s.toLowerCase().includes(skillFilter))) return false;
        return true;
    });
}


// ---------------- DISPLAY RESULTS ---------------- //
function displayResults(results) {

    const container = document.getElementById("results");
    container.innerHTML = "";

    let visibleCount = 0;

    results.forEach((r, index) => {

        visibleCount++;

        const skills = r.skills?.join(", ") || "N/A";
        const missing = r.missing_skills?.join(", ") || "None";
        const education = r.education?.join(", ") || "N/A";
        const experience = r.experience_years ?? 0;

        let badge = "";
        let cardClass = "result-item";

        if (index === 0) {
            badge = "<span style='color:green;'>🏆 Top Candidate</span><br>";
            cardClass += " top-candidate";
        }

        const div = document.createElement("div");
        div.className = cardClass;

        div.innerHTML = `
            <strong>${r.filename}</strong><br>
            ${badge}

            <b>Final Score:</b> ${r.final_score}%<br>
            <b>Skills:</b> ${skills}<br>
            <b>Missing Skills:</b> ${missing}<br>
            <b>Experience:</b> ${experience} years<br>
            <b>Education:</b> ${education}<br>

            <div class="progress">
                <div class="progress-bar" style="width:${r.final_score}%"></div>
            </div>
        `;

        container.appendChild(div);
    });

    if (visibleCount === 0) {
        container.innerHTML = `
            <p class="empty-message">
                No candidates match the selected filters.
            </p>
        `;
    }
}


// ---------------- CHARTS ---------------- //
let barChart, pieChart;

function renderCharts(results) {

    if (!results || results.length === 0) return;

    // 🔥 LIMIT DATA FOR PERFORMANCE
    const topResults = results.slice(0, 10);

    const labels = topResults.map(r => r.filename);
    const scores = topResults.map(r => r.final_score);

    if (barChart) barChart.destroy();
    if (pieChart) pieChart.destroy();

    barChart = new Chart(document.getElementById("barChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Match Score (%)",
                data: scores
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    pieChart = new Chart(document.getElementById("pieChart"), {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: scores
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}


// ---------------- DEBOUNCE ---------------- //
function debounce(func, delay) {
    let timeout;
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(func, delay);
    };
}


// ---------------- FILTER EVENTS ---------------- //
const applyFilters = () => {
    if (!window.lastResults) return;

    const filtered = getFilteredResults();
    displayResults(filtered);
    renderCharts(filtered);
};

document.getElementById("minScore").addEventListener("input", debounce(applyFilters, 300));
// ---------------- FILE PREVIEW ---------------- //
document.getElementById("files").addEventListener("change", function () {
    const files = Array.from(this.files);

    if (files.length === 0) {
        document.getElementById("fileNames").innerText = "";
        return;
    }

    const names = files.map(f => `${f.name} (${(f.size / 1024).toFixed(1)} KB)`);

    document.getElementById("fileNames").innerHTML =
        "<b>Uploaded:</b><br>" + names.join("<br>");
});


// ---------------- FORM SUBMIT ---------------- //
const form = document.getElementById("form");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const jd = document.getElementById("jd").value;
    const files = document.getElementById("files").files;

    if (!jd || files.length === 0) {
        alert("Please enter job description and upload resumes");
        return;
    }

    const formData = new FormData();
    formData.append("job_description", jd);

    for (let file of files) {
        formData.append("resumes", file);
    }

    const container = document.getElementById("results");
    container.innerHTML = `<div class="loading">Processing resumes...</div>`;

    const btn = document.querySelector("button");
    btn.disabled = true;
    btn.innerText = "Matching...";

    try {
        const response = await fetch("/match", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!data.success || !data.results) {
            container.innerHTML = `<p class="empty-message">No results returned</p>`;
            alert(data.error || "Something went wrong");
            return;
        }

        // Save globally
        window.lastResults = data.results;

        displayResults(data.results);
        renderCharts(data.results);

    } catch (error) {
        console.error(error);
        container.innerHTML = `<p class="empty-message">Server error occurred</p>`;
        alert("Error connecting to server");
    }

    btn.disabled = false;
    btn.innerText = "Match Resumes";
});


// ---------------- FILTER LOGIC ---------------- //
function getFilteredResults() {
    const minScore = parseFloat(document.getElementById("minScore").value) || 0;
    const skillFilter = document.getElementById("skillFilter").value.toLowerCase().trim();

    return window.lastResults.filter(r => {
        if (r.final_score < minScore) return false;
        if (skillFilter && !r.skills.some(s => s.toLowerCase().includes(skillFilter))) return false;
        return true;
    });
}


// ---------------- DISPLAY RESULTS ---------------- //
function displayResults(results) {

    const container = document.getElementById("results");
    container.innerHTML = "";

    let visibleCount = 0;

    results.forEach((r, index) => {

        visibleCount++;

        const skills = r.skills?.join(", ") || "N/A";
        const missing = r.missing_skills?.join(", ") || "None";
        const education = r.education?.join(", ") || "N/A";
        const experience = r.experience_years ?? 0;

        let badge = "";
        let cardClass = "result-item";

        if (index === 0) {
            badge = "<span style='color:green;'>🏆 Top Candidate</span><br>";
            cardClass += " top-candidate";
        }

        const div = document.createElement("div");
        div.className = cardClass;

        div.innerHTML = `
            <strong>${r.filename}</strong><br>
            ${badge}

            <b>Final Score:</b> ${r.final_score}%<br>
            <b>Skills:</b> ${skills}<br>
            <b>Missing Skills:</b> ${missing}<br>
            <b>Experience:</b> ${experience} years<br>
            <b>Education:</b> ${education}<br>

            <div class="progress">
                <div class="progress-bar" style="width:${r.final_score}%"></div>
            </div>
        `;

        container.appendChild(div);
    });

    if (visibleCount === 0) {
        container.innerHTML = `
            <p class="empty-message">
                No candidates match the selected filters.
            </p>
        `;
    }
}


// ---------------- CHARTS ---------------- //
let barChart, pieChart;

function renderCharts(results) {

    if (!results || results.length === 0) return;

    // 🔥 LIMIT DATA FOR PERFORMANCE
    const topResults = results.slice(0, 10);

    const labels = topResults.map(r => r.filename);
    const scores = topResults.map(r => r.final_score);

    if (barChart) barChart.destroy();
    if (pieChart) pieChart.destroy();

    barChart = new Chart(document.getElementById("barChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Match Score (%)",
                data: scores
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    pieChart = new Chart(document.getElementById("pieChart"), {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: scores
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}


// ---------------- DEBOUNCE ---------------- //
function debounce(func, delay) {
    let timeout;
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(func, delay);
    };
}


// ---------------- FILTER EVENTS ---------------- //
const applyFilters = () => {
    if (!window.lastResults) return;

    const filtered = getFilteredResults();
    displayResults(filtered);
    renderCharts(filtered);
};

document.getElementById("minScore").addEventListener("input", debounce(applyFilters, 300));
document.getElementById("skillFilter").addEventListener("input", debounce(applyFilters, 300));