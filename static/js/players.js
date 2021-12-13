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
  const listPlayersUrl = `/api/players?page=${page}&pageSize=${pageSize}`;
  $.ajax({
    url: listPlayersUrl,
    processData: false,
    contentType: false,
    type: 'GET',
    success: function (data) {
      listPlayers = data.content;
      // console.log(listPlayers[0]["age"]);
      const teamsDiv = $('.teams');
      // console.log(listPlayers[0]);
      for (var i = 0; i < listPlayers.length - 1; i = i + 2) {
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
        <a href="/player/${player1['id']}">
          <h5>
            <img
              src="${player1['photo_url']}"
              alt="${player1['name']}"
              class="player-img"
            />
            <span class="player-name">${player1['name']}</span>
          </h5>
          <img
            src="${player1['kickscore']}"
            alt="team-strength"
            class="team-strength"
            style='width: 500px;'
          />
        </a>
      </div>
    </div>
    <div class="col-hlf-ko">
      <!-- team link -->
      <div class="team-link team-one">
        <a href="/player/${player2['id']}">
          <h5>
            <img
              src="${player2['photo_url']}"
              alt="${player2['name']}"
              class="player-img"
            />
            <span class="player-name">${player2['name']}</span>
          </h5>
          <img
            src="${player2['kickscore']}"
            alt="team-strength"
            class="team-strength"
            style='width: 500px;'
          />
        </a>
      </div>
    </div>
  </div>
    `;
}
