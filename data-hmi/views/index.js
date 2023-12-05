// =============================================================================
// Constants
// =============================================================================
const BACKEND_URL = "http://" + window.location.host;

// =============================================================================
// Onload Ensures that the function is called once all the DOM elements of the page are ready to be used
// =============================================================================
$(async function () {

  $("#carousel div").on("click", function () {
    moveToSelected($(this));
  });

  $("#prev").on("click", function () {
    moveToSelected("prev");
  });

  $("#next").on("click", function () {
    moveToSelected("next");
  });

  //Make fixedquery when select changes:
  $('#fixedqueryselect').on('change', async function () {

    console.log($(this).val())
    switch ($(this).val()) {
      case '1':
        querysql = `SELECT match.id_match,date,place,ARRAY_AGG(team_name) AS "homeTeam vs awayTeam" FROM match
                    INNER JOIN disputes ON match.id_match = disputes.id_match
                    WHERE match.winner_team_ht = 'AwayTeam' AND match.winner_team_ft = 'HomeTeam'
                    GROUP BY match.id_match 
                    ORDER BY match.date ASC`
        break;
      case '2':
        querysql = `SELECT player.player_name, birthyear, nationality, position, COUNT(*) AS goals FROM player 
                    INNER JOIN goal ON goal.player_name = player.player_name
                    WHERE player.birthyear > 1985 AND (SELECT COUNT(*) FROM goal WHERE goal.player_name=player.player_name )>15
                    GROUP BY player.player_name
		    ORDER BY COUNT(*) DESC`
        break;
      case '3':
        querysql = `SELECT player.player_name, player.team_name, COUNT(*) AS yellow_cards FROM player 
                    INNER JOIN card ON card.player_name = player.player_name
                    WHERE card.type = 'Yellow'
                    GROUP BY player.player_name
                    ORDER BY COUNT(*) DESC
                    LIMIT 5`
        break;
      case '4':
        querysql = `SELECT team_name,
                    MIN(played_matches) played_matches,
                    MIN(wins) wins,
                    MIN(draws) draws,
                    MIN(losses) losses FROM ((SELECT disputes.team_name, COUNT(*) AS played_matches, NULL AS wins, CAST(NULL AS bigint) AS draws, CAST(NULL AS bigint) AS losses FROM match
                    INNER JOIN disputes ON match.id_match = disputes.id_match
                    GROUP BY disputes.team_name)
                    UNION
                    (SELECT disputes.team_name, NULL AS played_matches, COUNT(*) AS wins, CAST(NULL AS bigint) AS draws, CAST(NULL AS bigint) AS losses FROM match
                    INNER JOIN disputes ON match.id_match = disputes.id_match 
                    INNER JOIN team ON disputes.team_name = team.team_name
                    WHERE (match.winner_team_ft = 'HomeTeam' AND team.stadium = match.place) 
                    OR (match.winner_team_ft = 'AwayTeam' AND team.stadium != match.place)
                    GROUP BY disputes.team_name)
                    UNION 
                    (SELECT disputes.team_name, NULL AS played_matches, NULL AS wins, COUNT(*) AS "draws", CAST(NULL AS bigint) AS "losses" FROM match
                    INNER JOIN disputes ON match.id_match = disputes.id_match 
                    INNER JOIN team ON disputes.team_name = team.team_name
                    WHERE (match.winner_team_ft = 'Draw' AND team.stadium = match.place) 
                    OR (match.winner_team_ft = 'Draw' AND team.stadium != match.place)
                    GROUP BY disputes.team_name)
                    UNION
                    (SELECT disputes.team_name, NULL AS played_matches, NULL AS wins, CAST(NULL AS bigint) AS "draws", COUNT(*) AS "losses" FROM match
                    INNER JOIN disputes ON match.id_match = disputes.id_match 
                    INNER JOIN team ON disputes.team_name = team.team_name
                    WHERE (match.winner_team_ft = 'AwayTeam' AND team.stadium = match.place) 
                    OR (match.winner_team_ft = 'HomeTeam' AND team.stadium != match.place)
                    GROUP BY disputes.team_name))
                    GROUP BY team_name
                    ORDER BY wins DESC
                  `
        break;
    }

    $.ajax({
      url: BACKEND_URL + "/sqlquery",
      type: 'POST',
      data: JSON.stringify({ query: querysql.replace(/(\r\n|\n|\r)/gm, "") }),
      processData: false,
      dataType: 'json',
      crossDomain: true,
      async: true,
      contentType: "application/json",
      success: function (response) {
        tablehtml = `<thead class="thead-dark">
                        <tr>`
        response.fields.forEach(field => { tablehtml = tablehtml.concat(' <th scope="col">' + field.name + '</th>') })
        tablehtml = tablehtml.concat(' </tr> </thead> <tbody>')
        response.rows.forEach(field => {
          tablehtml = tablehtml.concat(' <tr>')
          for (var key in field) {
            if (key == 'date') tablehtml = tablehtml.concat('<td>' + field[key].split('T')[0] + '</td>');
            else tablehtml = tablehtml.concat('<td>' + field[key] + '</td>');
          }
          tablehtml = tablehtml.concat(' </tr>')
        })
        tablehtml = tablehtml.concat('</tbody>')
        $('#fixedquerytable').html(tablehtml)
      },

      error: function () {
        alert("Something went wrong with your query :(");
      }
    });
  })


  $("#newqueryButton").on("click", function () {
    $.ajax({
      url: BACKEND_URL + "/sqlquery",
      type: 'POST',
      data: JSON.stringify({ query: $('#newquerytextarea').val().replace(/(\r\n|\n|\r)/gm, "") }),
      processData: false,
      dataType: 'json',
      crossDomain: true,
      async: true,
      contentType: "application/json",
      success: function (response) {
        if (response.rows.length == 0) alert("There is no data matching your query :(");
        tablehtml = `<thead class="thead-dark">
                        <tr>`
        response.fields.forEach(field => { tablehtml = tablehtml.concat(' <th scope="col">' + field.name + '</th>') })
        tablehtml = tablehtml.concat(' </tr> </thead> <tbody>')
        response.rows.forEach(field => {
          tablehtml = tablehtml.concat(' <tr>')
          for (var key in field) {
            if (key == 'date') tablehtml = tablehtml.concat('<td>' + field[key].split('T')[0] + '</td>');
            else tablehtml = tablehtml.concat('<td>' + field[key] + '</td>');
          }
          tablehtml = tablehtml.concat(' </tr>')
        })
        tablehtml = tablehtml.concat('</tbody>')
        $('#newquerytable').html(tablehtml)
      },

      error: function () {
        alert("Something went wrong with your query :(");
      }
    });
  })

  $(".team").on("click", function () {
    $.ajax({
      url: BACKEND_URL + "/sqlquery",
      type: 'POST',
      data: JSON.stringify({ query: "SELECT * FROM team WHERE team_name='" + $(this).attr('id') + "'" }),
      processData: false,
      dataType: 'json',
      crossDomain: true,
      async: true,
      contentType: "application/json",
      success: function (response) {
        if (response.rows.length == 0) alert("There is no data matching your query :(");
        tablehtml = `<thead class="thead-dark">
                          <tr>`
        response.fields.forEach(field => { tablehtml = tablehtml.concat(' <th scope="col">' + field.name + '</th>') })
        tablehtml = tablehtml.concat(' </tr> </thead> <tbody>')
        response.rows.forEach(field => {
          tablehtml = tablehtml.concat(' <tr>')
          for (var key in field) {
            if (key == 'date') tablehtml = tablehtml.concat('<td>' + field[key].split('T')[0] + '</td>');
            else tablehtml = tablehtml.concat('<td>' + field[key] + '</td>');
          }
          tablehtml = tablehtml.concat(' </tr>')
        })
        tablehtml = tablehtml.concat('</tbody>')
        $('#teamtable').html(tablehtml)
      },

      error: function () {
        alert("Something went wrong with your query :(");
      },
      complete: function () {
        window.scrollTo(0, document.body.scrollHeight);
      }
    });
  })

})



function moveToSelected(element) {
  if (element == "next") {
    var selected = $(".selected").next();
  } else if (element == "prev") {
    var selected = $(".selected").prev();
  } else {
    var selected = element;
  }

  var next = $(selected).next();
  var prev = $(selected).prev();
  var prevSecond = $(prev).prev();
  var nextSecond = $(next).next();

  $(selected).removeClass().addClass("selected team");

  $(prev).removeClass().addClass("prev  team");
  $(next).removeClass().addClass("next  team");

  $(nextSecond).removeClass().addClass("nextRightSecond  team");
  $(prevSecond).removeClass().addClass("prevLeftSecond  team");

  $(nextSecond).nextAll().removeClass().addClass("hideRight  team");
  $(prevSecond).prevAll().removeClass().addClass("hideLeft  team");
}

// Eventos teclado
$(document).keydown(function (e) {
  switch (e.which) {
    case 37: // left
      moveToSelected("prev");
      $(".selected").click()
      break;

    case 39: // right
      moveToSelected("next");
      $(".selected").click()
      break;

    default:
      return;
  }
  e.preventDefault();
});
