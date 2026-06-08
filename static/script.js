let chart;

async function runBenchmark() {

    const size =
        document.getElementById("size").value;

    const response = await fetch("/benchmark", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            size: size
        })

    });

    const data = await response.json();

    document.getElementById("normal")
        .innerText = data.normal + " s";

    document.getElementById("parallel")
        .innerText = data.parallel + " s";

    document.getElementById("speedup")
        .innerText = data.speedup + "x";

    if(chart){
        chart.destroy();
    }

    chart = new Chart(
        document.getElementById("chart"),
        {
            type:"bar",
            data:{
                labels:[
                    "Normal",
                    "Parallel"
                ],
                datasets:[{
                    label:"Execution Time",
                    data:[
                        data.normal,
                        data.parallel
                    ]
                }]
            }
        }
    );
}
