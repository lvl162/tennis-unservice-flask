/*

matchId, player1, player2, date 

player1{
  name, img, prob,
}

*/
let currentPage = 0;

$(document).ready(() => {
  // const resultContainer = $('.result-matches-container');
  getPastMatches(currentPage, 5);
  getUpcomingMatches(currentPage, 5);
  
  $('.more-matches-all').click(() => {
    currentPage +=1
    getPastMatches(currentPage, 5);
    getUpcomingMatches(currentPage, 5);

  });
});

const getPastMatches = (page, pageSize) => {
  const resultContainer = $('.result-matches-container');

  const getMoreCommentsUrl = `/api/pastresult?page=${page}&pageSize=${pageSize}`;
  $.ajax({
    url: getMoreCommentsUrl,
    // headers: {
    //   [header]: token,
    // },
    processData: false,
    contentType: false,
    type: 'GET',
    success: function (data) {
      const matches = data.content;
      const html = matches.map(
        ({
          id,
          date,
          player1,
          player2,
          surface,
          tourney_name,
          tourney_level,
          winner_id,
        }) => {
          return resultMatchTemplate(id, player1, player2, date, winner_id);
        }
      );
      resultContainer.append(html);
    },
    error: function (err) {
      // showError('Email already existed');
      console.log(err);
    },
  });
};

const getUpcomingMatches = (page, pageSize) => {
  const fixtureContainer = $('.fixture-matches-container');
  const getMoreCommentsUrl = `/api/upcoming?page=${page}&pageSize=${pageSize}`;
  $.ajax({
    url: getMoreCommentsUrl,
    // headers: {
    //   [header]: token,
    // },
    processData: false,
    contentType: false,
    type: 'GET',
    success: function (data) {
      const matches = data.content;
      const html = matches.map(
        ({
          id,
          date,
          player1,
          player2,
          surface,
          tourney_name,
          tourney_level,
        }) => {
          console.log(player1, player2);
          return fixtureMatchTemplate(id, player1, player2, date);
        }
      );
      fixtureContainer.append(html);
    },
    error: function (err) {
      console.log(err);
    },
  });
};
