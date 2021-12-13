```

create table if not exists matches (
	id serial primary key,
	player_1_id int,
	player_2_id int, 
    player_1_rank int,
    player_2_rank int,
    player_1_rank_points float,
    player_1_prob float,
    player_2_prob float,
    player_2_rank_points int,
	tourney_date date,
    tourney_level varchar(10),
	surface varchar(20),
	winner_id int,
	tourney_name varchar(50),
    finished boolean default true,
	CONSTRAINT fk_players_winner
      FOREIGN KEY(player_1_id)
	  REFERENCES players(id), 
	CONSTRAINT fk_players_loser
      FOREIGN KEY(player_2_id)
	  REFERENCES players(id)
);


create table if not exists ranks(
	id serial primary key,
	player_id int,
	ranking_date date,
	rank int,
	points int,
	CONSTRAINT fk_players_id
      FOREIGN KEY(player_id)
	  REFERENCES players(id)
)

/// 

select m.*, p1.name as player_1_name, p2.name as player_2_name, p1.photo_url as player_1_photo_url, p2.photo_url as player_2_photo_url from matches m inner join players p1 on m.player_1_id=p1.id
inner join players p2 on m.player_2_id=p2.id

order by m.id asc limit 100

```




