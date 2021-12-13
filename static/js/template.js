const resultMatchTemplate = (matchId, player1, player2, date, winner_id) => {
    const winnerPred = player1.prob > player2.prob ? player1.id : player2.id;
  const wrong = winnerPred != winner_id;
  const template = `
    <div class="prediction prediction-fixture">
    <a href="/match/${matchId}">
    <div class="player-1">
        <img src="${player1.photo_url}"
            alt="${player1.name}" class="player-img">
        <span class="player-name">${player1.name}</span>
    </div>
    <div class="prediction-details">
    <div class="prediction-percentages">
        <span class="${
          player1.prob < player2.prob ? 'text-scale-200' : 'text-scale-100'
        } ${
          player1.prob > player2.prob && wrong ? 'text-scale-200' : ''
        }
        ${
          player1.prob < player2.prob && wrong ? 'text-scale-300' : ''
        }
        
        ">${Math.floor(player1.prob * 100)}%</span>
        <span class="${wrong ? "wrong-prediction text-scale-300" :'text-scale-100'}">${wrong ? "That's quite a surprise" :'We made the right call'}</span>
        <span class="${
          player1.prob > player2.prob ? 'text-scale-200' : 'text-scale-100'
        } ${
          player1.prob < player2.prob && wrong ? 'text-scale-200' : ''
        }
        ${
          player1.prob > player2.prob && wrong ? 'text-scale-300' : ''
        }
        ">${Math.floor(player2.prob * 100)}%</span>
    </div>
            ${resultProgressBar(player1, player2, wrong)}
            <div class="match-time-list">${dateFormat(date)}</div>
        </div>
        <div class="player-2">
            <span class="player-name">${player2.name}</span>
            <img src="${player2.photo_url}"
            alt="${player2.name}" class="player-img">
        </div>
    </a>
</div>
      `;
  return template;
};

const fixtureMatchTemplate = (matchId, player1, player2, date) => {
  // const winnerName = player1.prob > player2.prob
  // ? player1.name
  // : player2.name;
  const winnerPct = Math.floor(
    player1.prob > player2.prob ? player1.prob * 100 : player2.prob * 100
  );
  const template = `
      <div class="prediction prediction-fixture">
                          <a href="/match/${matchId}">
                              <div class="player-1">
                                  <img src="${player1.photo_url}"
                                      alt="${player1.name}" class="player-img">
                                  <span class="player-name">${
                                    player1.name
                                  }</span>
                              </div>
                              <div class="prediction-details">
                                  <div class="prediction-percentages">
                                      <span class="${
                                        player1.prob < player2.prob ? 'text-scale-200' : 'text-scale-100'
                                      } ">${Math.floor(
    player1.prob * 100
  )}%</span>
                                      <span class="${
                                        player1.prob > player2.prob ? 'text-scale-200' : 'text-scale-100'

                                      } ">${Math.floor(
    player2.prob * 100
  )}%</span>
                                  </div>
                                  ${fixtureProgressBar(player1, player2)}
                                  <div class="match-time-list">${dateFormat(date)}</div>
                              </div>
                              <div class="player-2">
                                  <span class="player-name">${
                                    player2.name
                                  }</span>
                                  <img src="${player2.photo_url}"
                                      alt="${player2.name}" class="player-img">
                              </div>
                          </a>
                      </div>
      `;
  return template;
};

const fixtureProgressBar = (player1, player2) => {
  const winnerPct = Math.floor(
    player1.prob > player2.prob ? player1.prob * 100 : player2.prob * 100
  );
  return player1.prob > player2.prob
    ? `<div class="progress bg-gray-400">
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
    : `<div class="progress bg-gray-400">
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
