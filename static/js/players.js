var pageSize = 10;
var page = 0;
$(document).ready(() => {
  //   console.log("oke");
  getListPlayers(pageSize, page);

  $(document).on('click', '#show-more', function (e) {
    page = page + 1;
    getListPlayers(pageSize, page);
  });
});

const getListPlayers = (pageSize, page) => {
  const listPlayersUrl = `https://api.wtatennis.com/content/wta/photo/EN/?pageSize=${pageSize}&page=${page}&tagNames=player-headshot`;

  console.log(listPlayersUrl);
  $.ajax({
    url: listPlayersUrl,
    processData: false,
    contentType: false,
    type: 'GET',
    success: function (data) {
      listPlayers = data.content;
      const teamsDiv = $('.teams');
      for (var i = 0; i < listPlayers.length - 1; i = i + 2) {
        // console.log(listPlayers[i]["references"][0]['sid']);
        teamsDiv.append(
          templateListPlayers(listPlayers[i], listPlayers[i + 1])
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
};

function templateListPlayers(player1, player2) {
  return ` <div class="container-ko clearfix">
    <div class="col-hlf-ko">
      <!-- team link -->
      <div class="team-link team-one">
        <a href="/player/${player1['references'][0]['sid']}">
          <h5>
            <img
              src="${player1['imageUrl']}"
              alt="${player1['title']}"
              class="player-img"
            />
            <span class="player-name">${player1['title']}</span>
          </h5>
          <img
            src="https://kickoff.ai/static/img/sparklines/83.svg"
            alt="team-strength"
            class="team-strength"
          />
        </a>
      </div>
    </div>
    <div class="col-hlf-ko">
      <!-- team link -->
      <div class="team-link team-one">
        <a href="/player/${player2['references'][0]['sid']}">
          <h5>
            <img
              src="${player2['imageUrl']}"
              alt="${player2['title']}"
              class="player-img"
            />
            <span class="player-name">${player2['title']}</span>
          </h5>
          <img
            src="https://kickoff.ai/static/img/sparklines/83.svg"
            alt="team-strength"
            class="team-strength"
          />
        </a>
      </div>
    </div>
  </div>
    `;
}
