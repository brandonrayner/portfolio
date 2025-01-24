var frogcounter = 0;
var orangecounter = 0;
var skeletoncounter = 0;
var battlegrid_player = [[null,null,null],[null,null,null],[null,null,null]];
var battlegrid_enemy = [[null,null,null],[null,null,null],[null,null,null]];
var battlegrid_selected = null;
var globalcount = 0;
var tickrate = 1000;
var gameActive = true;


function getfrog(number){
    frogcounter++;
    document.getElementById("frogcount").innerHTML = "You have "+frogcounter+" frogs";
};

function getorange(number){
    orangecounter++;
    document.getElementById("orangecount").innerHTML = "You have "+orangecounter+" oranges";
};

function getskeleton(number){
    skeletoncounter++;
    document.getElementById("skeletoncount").innerHTML = "You have "+skeletoncounter+" skeletons";
};

function tabactive(tabname){
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  };

  tabcontent = document.getElementById(tabname);
  tabcontent.style.display = "block";
};

function battlegrid_setcell(location, content){
  var findcell;
  findcell = document.getElementById(location);
  if (content == "frog"){
    findcell.innerHTML = "<img style='width:50px;height:50px' src='frog.jpg' >";
  };
  if (content == "orange"){
    findcell.innerHTML = "<img style='width:50px;height:50px' src='orange.jpg' >";
  };
  if (content == "skeleton"){
    findcell.innerHTML = "<img style='width:50px;height:50px' src='skeleton.png' >";
  };
  if (content == "none"){
    findcell.innerHTML = location;
  };
}

function battlegrid_update(){
  var i, j;
  for (i = 0; i < battlegrid_player.length; i++) {
  	for (j = 0; j < battlegrid_player.length; j++) {
  	  if (battlegrid_player[i][j]){
        battlegrid_setcell("P"+i+j, battlegrid_player[i][j]);
  	  } else {
  	    battlegrid_setcell("P"+i+j, "none");
  	  };
  	};
  };
  for (i = 0; i < battlegrid_enemy.length; i++) {
  	for (j = 0; j < battlegrid_player.length; j++) {
  	  if (battlegrid_enemy[i][j]){
        battlegrid_setcell("E"+i+j, battlegrid_enemy[i][j]);
  	  } else {
  	    battlegrid_setcell("E"+i+j, "none");
  	  };
  	};
  };
};

function cell_select(location){
  var cell_owner = location[0];
  var cell_col = location[1];
  var cell_row = location[2];
  findcell = document.getElementById(location);
  if (battlegrid_selected) {
  	var cell_owner_old = battlegrid_selected[0];
  	var cell_col_old = battlegrid_selected[1];
    var cell_row_old = battlegrid_selected[2];
    var storage;
  	if (cell_owner == "P" && cell_owner_old == "P"){
      storage = battlegrid_player[cell_col][cell_row];
      battlegrid_player[cell_col][cell_row] = battlegrid_player[cell_col_old][cell_row_old];
      battlegrid_player[cell_col_old][cell_row_old] = storage;
  	};
    oldcell = document.getElementById(battlegrid_selected);
    oldcell.style.background = "#FFFFFF";
    battlegrid_selected = null;
  } else {
  	findcell.style.background = "#CCAAAA";
    battlegrid_selected = location;
  };
  battlegrid_update();
};

function sleep(ms){
  return new Promise(resolve => setTimeout(resolve, ms));
};

async function gameLoop(){
  while (true){
    await sleep(tickrate);
    if(gameActive){
      // console.log('ticking');
      globalcount++;
      document.getElementById("loopcounter").innerHTML = "Counter is "+globalcount;
    };
  };
};

function gameLoopPause(){
  gameActive = !gameActive;
};

function gameLoopSpeed(ms){
  tickrate = ms;
};

function initialize(){
  battlegrid_player[0][0] = "frog";
  battlegrid_player[1][2] = "orange";
  battlegrid_enemy[1][1] = "skeleton";
  battlegrid_update();
  gameLoop();
};