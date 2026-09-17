var frogcounter = 0;

var day = 1;
var health = 100;
var hunger = 100;
var thirst = 100;
var warmth = 100;


function getfrog(number){
    frogcounter++;
    document.getElementById("frogcount").innerHTML = "You have "+frogcounter+" frogs";
}

function timePasses(){
    hunger = hunger - 10;
    thirst = thirst - 10;
    warmth = warmth - 10;
}

function updateStatus(){
    document.getElementById("day").innerHTML = "Day: "+day ;
    document.getElementById("health").innerHTML = "Health: "+health +"%";
    document.getElementById("hunger").innerHTML = "Hunger: "+hunger +"%";
    document.getElementById("thirst").innerHTML = "Thirst: "+thirst +"%";
    document.getElementById("warmth").innerHTML = "Warmth: "+warmth +"%";
}

function getFood(){
    timePasses();
    hunger = 100;
    thirst = 100;
    updateStatus();
}

function getMaterials(){
    timePasses();
    updateStatus();
}

function getShelter(){
    timePasses();
    warmth = 100;
    updateStatus();
}

function getSleep(){
    timePasses();
    day++;
    health = 100;
    updateStatus();
}
