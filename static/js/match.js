$(document).ready(function () {

  $('.result-bar-container').html(
    templateMatch(player1, player2, date, tourney_name, tourney_level, winner_id)
  );

});

const templateMatch = (player1, player2, date, tourney_name, tourney_level, winner_id) => {
  const winnerPred = player1.prob > player2.prob ? player1.id : player2.id;
  const wrong = winnerPred != winner_id;
  const winnerPct = Math.floor(
    player1.prob > player2.prob ? player1.prob * 100 : player2.prob * 100
  );
  return `
    <div class="perdiction prediction-fixture m-5">
                <div class="prediction-details">
                    <div class="prediction-percentages">
                        <span class="prediction-1st-win ${
                          player1.prob < player2.prob ? 'text-scale-200' : 'text-scale-100'
                        } ${
                          player1.prob > player2.prob && wrong ? 'text-scale-200' : ''
                        }
                        ${
                          player1.prob < player2.prob && wrong ? 'text-scale-300' : ''
                        }">${Math.floor(
                          player1.prob * 100
                        )}%</span>
                        <span class="prediction-2nd-win ${
                          player1.prob > player2.prob ? 'text-scale-200' : 'text-scale-100'
                        } ${
                          player1.prob < player2.prob && wrong ? 'text-scale-200' : ''
                        }
                        ${
                          player1.prob > player2.prob && wrong ? 'text-scale-300' : ''
                        }">${Math.floor(
                          player2.prob * 100
                        )}%</span>
                    </div>
                   ${resultProgressBar(player1, player2, wrong)}
                    <div class="match-details">
                        <div class="matchtime">${dateFormat(date)}</div>
                        <div href="#" class="match-competition">${tourney_level}</div>
                        <div class="match-location">${tourney_name}</div>
                    </div>
                </div>
            </div>

    `;
};

const fixtureProgressBar = (player1, player2) => {
  const winnerPct = Math.floor(
    player1.prob > player2.prob ? player1.prob * 100 : player2.prob * 100
  );
  return player1.prob > player2.prob
    ? `<div class="progress bg-gray-400 big-bar">
                                        <div class="progress-bar bg-gray-100" role="progressbar" style="width: ${winnerPct}%"
                                            aria-valuenow="${winnerPct}" aria-valuemin="0" aria-valuemax="100"
                                            data-toggle="tooltip"
                                            data-html="true" data-placement="top"
                                            title="Most likely result: ${
                                              player1.name
                                            } wins (${winnerPct} %)"
                                            ></div>
                                        <div class="progress-bar bg-scale-300" role="progressbar" style="width: ${
                                          100 - winnerPct
                                        }%"
                                            aria-valuenow="${
                                              100 - winnerPct
                                            }" aria-valuemin="0" aria-valuemax="100" ></div>
                                    </div>`
    : `<div class="progress bg-gray-400 big-bar">
        <div class="progress-bar bg-scale-300" role="progressbar" style="width: ${
          100 - winnerPct
        }%"
              aria-valuenow="${
                100 - winnerPct
              }" aria-valuemin="0" aria-valuemax="100" ></div>
                                    <div class="progress-bar bg-gray-100" role="progressbar" style="width: ${winnerPct}%"
                                        aria-valuenow="${winnerPct}" aria-valuemin="0" aria-valuemax="100"
                                        data-toggle="tooltip"
                                        data-html="true" data-placement="top"
                                        title="Most likely result: ${
                                          player2.name
                                        } wins (${winnerPct} %)"
                                        ></div>
                                    
                                </div>`;
};

const resultProgressBar = (player1, player2, wrong) => {
  
  const winnerPct = Math.floor(
    player1.prob > player2.prob ? player1.prob * 100 : player2.prob * 100
  );

  // wrong 

  // player1 win 

  // player2 win
  return player1.prob > player2.prob
    ? `<div class="progress bg-gray-400">
                                      <div class="progress-bar ${
                                        wrong ? 'bg-gray-300' : 'bg-gray-100'
                                      } " role="progressbar" style="width: ${winnerPct}%"
                                          aria-valuenow="${winnerPct}" aria-valuemin="0" aria-valuemax="100"
                                          data-toggle="tooltip"
                                          data-html="true" data-placement="top"
                                          title="Most likely result: ${
                                            player1.name
                                          } wins (${winnerPct} %)"
                                          ></div>
                                      <div class="progress-bar ${
                                        wrong ? 'wrong-answer' : ''
                                      }" role="progressbar" style="width: ${
                                        100 - winnerPct
                                      }%"
                                          aria-valuenow="${
                                            100 - winnerPct
                                          }" aria-valuemin="0" aria-valuemax="100" ></div>
                                  </div>`
    : `<div class="progress bg-gray-400">
      <div class="progress-bar ${
        wrong ? 'wrong-answer' : ''
      }" role="progressbar" style="width: ${
        100 - winnerPct
      }%"
            aria-valuenow="${
              100 - winnerPct
            }" aria-valuemin="0" aria-valuemax="100" ></div>
                                  <div class="progress-bar ${
                                    wrong ? 'bg-gray-300' : 'bg-gray-100'
                                  }" role="progressbar" style="width: ${winnerPct}%"
                                      aria-valuenow="${winnerPct}" aria-valuemin="0" aria-valuemax="100"
                                      data-toggle="tooltip"
                                      data-html="true" data-placement="top"
                                      title="Most likely result: ${
                                        player2.name
                                      } wins (${winnerPct} %)"
                                      ></div>
                                  
                              </div>`;
};
