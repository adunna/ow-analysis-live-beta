const colors = [
  "#e6194b",
  "#3cb44b",
  "#ffe119",
  "#4363d8",
  "#f58231",
  "#911eb4",
  "#46f0f0",
  "#f032e6",
  "#bcf60c",
  "#fabebe",
  "#008080",
  "#e6beff",
];

var data = {
  datasets: [],
};

var config = {
  type: "line",
  data: data,
  options: {
    scales: {
      x: {
        type: "timeseries",
        time: {
          unit: "minute",
        },
        title: {
          color: "#000",
          display: true,
          text: "Match Time Elapsed",
        },
      },
      y: {
        title: {
          color: "#000",
          display: true,
          text: "Impact Score",
        },
      },
    },
    elements: {
      point: {
        radius: 0,
      },
    },
    plugins: {
      title: {
        display: true,
        text: "Impact Score of Players over Time",
      },
    },
  },
};

var impactScoreChart = new Chart(
  document.getElementById("impactScoreChart"),
  config
);

setInterval(function () {
  $.getJSON("data_json", function (data) {
    $("#game-map").html(data.Map);
    $("#game-stats-mode").html(data.StatsMode);
    $("#game-map-time").html(data.Duration);
    $("#team1-name").html(data.Teams[0]);
    $("#team2-name").html(data.Teams[1]);
    if (data.DurationInSeconds > 0) {
      for (let team = 0; team < 2; team++) {
        for (let player = 0; player < 6; player++) {
          if (impactScoreChart.data.datasets.length < 12) {
            impactScoreChart.data.datasets.push({
              label: data.PlayerStats[team][player].Name,
              backgroundColor: colors[team * 6 + player],
              borderColor: colors[team * 6 + player],
              data: [],
              borderWidth: 1,
            });
          }
          impactScoreChart.data.datasets[team * 6 + player].data.push(
            data.ImpactScoreChartFormat[team][player]
          );
        }
      }
      impactScoreChart.update();
    }
  });
}, 1000);

$(function () {
  for (let i = 1; i < 3; i++) {
    $("#table" + i).bootstrapTable({
      classes: "table table-bordered table-hover table-striped table-sm",
    });
  }
  $("#table-delta-impact-scores").bootstrapTable();
});

$("#toggle10").on("click", function (e) {
  e.preventDefault();
  $.ajax({ type: "GET", url: "/toggle_per_10" });
});
