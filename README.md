# Desert Strike

This game is a copy of a Starcraft 2 arcade mode called "Desert Strike".

For the zip file with the .exe go to:
https://www.dropbox.com/s/3ahv05gv5gqzikg/desert-strike.zip?dl=0

I want to recreate it using pygame.

### Plan:
* Have a battlefield
  * tiles for units (done)
  * area for unit spawns (done)
  * scrolling
  * more than 2 players
* Have units spawn
  * "ghost" units dont walk (done)
  * "ghosts" get copied on round start (done)
  * ability to move units in spawn area (done)
  * good looking buttons
* Have units walk towars eachother and fight
  * track position / collisions (done)
  * move (done)
  * find valid attack targets (done)
  * attack (done)
  * have target die (done)
  * aggro instead of just walk
* Have good UI
  * Self explanatory buttons (kinda done)
  * Player info
  * Round info
* Have muliplayer
  * local
  * online

### Image:
![title_img](https://user-images.githubusercontent.com/76616229/124322014-fce28d00-db7e-11eb-9398-618e67d95051.png)

_I know it looks terrible, this is the first time I tried making anything wiht pygame._


### Controls:
* To spawn a unit: Left click on the button then right click in the spawn area of either team (the gray tiles).
* To move a unit: Left click the unit, then right click where you want it to go. _(I know the hitboxes don't quite match the tiles)_
* Mouse over a "ghost" unit to see some stats. Mouse over "live" unit for HP.
* Also: There is interest, saving money may be worth it. 
