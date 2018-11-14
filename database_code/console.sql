CREATE TABLE PLAYERS (
  id int(8) NOT NULL,
  username varchar(32),
  nickname varchar(32),
  sex int(1),
  race int(1),
  fraction varchar(6),
  class varchar(6),

  exp int(4),
  lvl int(4),
  free_points int(4),
  fatigue int(1),

  endurance int(4),
  power int(4),
  armor int(4),
  mana_points int(4),
  agility int(4),

  mana int(4),
  hp int(4),

  location int(1),

  gold int(8),
  metal int(8),
  wood int(8),

  head varchar(10),
  body varchar(10),
  shoulders varchar(10),
  legs varchar(10),
  feet varchar(10),
  left_arm varchar(10),
  right_arm varchar(10),
  mount varchar(10)

);


create table equipment
(
  type        varchar(1)  not null,
  id          int(4)      not null,
  name        varchar(32) null,
  endurance   int(4)      null,
  power       int(4)      null,
  armor       int(4)      null,
  mana_points int(4)      null,
  agility     int(4)      null
);