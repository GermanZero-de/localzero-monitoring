(async () => {
  const response = await fetch("/api/mstr/" + LZM.city.municipalityKey);

  const el = document.querySelector("#kpiPV .canvas");
  if (!el) return;

  if (!response.ok) {
    el.innerHTML =
      "Fehler beim Laden der Daten aus dem Marktstammdatenregister.";
    return;
  }

  const data = await response.json();
  const options = {
    annotations: {
      xaxis: [
        {
          x: LZM.city.resolutionYear,
          label: {
            text: "Grundsatzbeschluss",
          },
        },
      ],
      points: [
        {
          y: data["installed"][data["installed"].length - 1],
          x: 2035,
          label: {
            text: data["installed"][data["installed"].length - 1],
          },
        },
      ],
    },

    series: [
      {
        name: "Bisher",
        type: "column",
        data: data["installed"],
      },
    ],
    chart: {
      width: "100%",
      type: "line",
      zoom: {
        enabled: false,
      },
    },
    forecastDataPoints: {
      count: 14,
    },
    colors: ["#234fad", "#ed8f47"],
    stroke: {
      width: [0, 5],
    },
    dataLabels: {
      enabled: false,
    },
    grid: {
      row: {
        colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    labels: data["years"],
    xaxis: {},
  };

  el.innerHTML = null;
  const chart = new ApexCharts(el, options);
  chart.render();
})();
