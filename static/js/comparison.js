let comparisonChart = null;

function loadCities() {

    fetch("/api/cities?year=all")
        .then(res => res.json())
        .then(data => {

            const city1 = document.getElementById("city1");
            const city2 = document.getElementById("city2");

            city1.innerHTML = "";
            city2.innerHTML = "";

            data.cities.forEach(c => {
                city1.innerHTML += `<option value="${c}">${c}</option>`;
                city2.innerHTML += `<option value="${c}">${c}</option>`;
            });
        });
}

function loadComparison() {

    const year   = document.getElementById("yearFilter").value;
    const city1  = document.getElementById("city1").value;
    const city2  = document.getElementById("city2").value;
    const age    = document.getElementById("ageFilter").value;
    const gender = document.getElementById("genderFilter").value;

    fetch(`/api/city-vs-city?year=${year}&city1=${city1}&city2=${city2}&age=${age}&gender=${gender}`)
        .then(res => res.json())
        .then(data => {

            if (comparisonChart) comparisonChart.destroy();

            comparisonChart = new Chart(
                document.getElementById("comparisonChart"),
                {
                    type: "bar",
                    data: {
                        labels: Object.keys(data),
                        datasets: [{
                            data: Object.values(data),
                            borderRadius: 8,
                            barThickness: 80
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                }
            );
        });
}

document.addEventListener("DOMContentLoaded", () => {

    loadCities();

    document.querySelectorAll("select").forEach(sel => {
        sel.addEventListener("change", loadComparison);
    });

    loadComparison();
});
