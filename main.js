let chart;

function updateData() {
    fetch("/data")
    .then(res => res.json())
    .then(data => {

        const normalDiv = document.getElementById("normal");
        const attackDiv = document.getElementById("attacks");

        // ✅ Always show something
        normalDiv.innerHTML = data.normal.length
            ? data.normal.map(t => `<p>${t}</p>`).join("")
            : "<p>No normal traffic</p>";

        attackDiv.innerHTML = data.attacks.length
            ? data.attacks.map(t => `<p style="color:red;">${t}</p>`).join("")
            : "<p>No attacks</p>";

        document.getElementById("accuracy").innerText =
            "Accuracy: " + data.stats.accuracy + "%";

        // ❌ ALERT REMOVED (NO POPUP)

        // ✅ GRAPH FIX
        const normalCount = data.normal.length;
        const attackCount = data.attacks.length;

        const ctx = document.getElementById("attackChart");

        if (!ctx) return;  // 🔥 prevents crash if element missing

        if (!chart) {
            chart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["Normal", "Attacks"],
                    datasets: [{
                        label: "Traffic",
                        data: [normalCount, attackCount]
                    }]
                }
            });
        } else {
            chart.data.datasets[0].data = [normalCount, attackCount];
            chart.update();
        }

    })
    .catch(err => console.log("Error:", err)); // 🔥 prevents crash
}

setInterval(updateData, 2000);