setInterval(function () {
  $.getJSON("data_json", function (data) {
    $("#game-map").html(data.Map);
    $("#game-stats-mode").html(data.StatsMode);
    $("#game-map-time").html(data.DurationInSeconds);
    $("#team1-name").html(data.Teams[0]);
    $("#team2-name").html(data.Teams[1]);
  });
}, 2000);

$(function () {
  $("#table1").bootstrapTable();
  $("#table2").bootstrapTable();
});

$("#toggle10").on("click", function (e) {
  e.preventDefault();
  $.ajax({ type: "GET", url: "/toggle_per_10" });
});
