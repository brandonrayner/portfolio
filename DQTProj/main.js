var counter = 0;

function myFunction(number){
    counter = counter + number;
    document.getElementById("count").innerHTML = counter;
};

var selectrow = 1;

function selectme(number){
    selectrow = number
    rowid = "mon" + number
    document.getElementById("mon1").style.background = "#ffda75";
    document.getElementById("mon2").style.background = "#ffde85";
    document.getElementById("mon3").style.background = "#ffda75";
    document.getElementById("mon4").style.background = "#ffde85";
    document.getElementById("mon5").style.background = "#ffda75";
    
    document.getElementById(rowid).style.background = "#FCAA00";
}

function getresistance(element, value){
    if (value === 1){
        element.innerHTML = "H";
        element.style.fontWeight = "900";
        element.style.color = "#6666FF";
        element.style.fontSize = "x-large";
        element.style.textShadow = "0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000";
    } else if (value === 2) {
        element.innerHTML = "-";
        element.style.fontWeight = "900";
        element.style.color = "#000000";
        element.style.fontSize = "x-large";
        element.style.textShadow = "0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000";
    } else if (value === 3) {
        element.innerHTML = "O";
        element.style.fontWeight = "900";
        element.style.color = "#FFFF00";
        element.style.fontSize = "x-large";
        element.style.textShadow = "0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000";
    } else {
        element.innerHTML = "X";
        element.style.fontWeight = "900";
        element.style.color = "#FF0000";
        element.style.fontSize = "x-large";
        element.style.textShadow = "0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000, 0px 0px 1px #000000";
    }
    
}

function selectunit(unitid){
    document.getElementById("mon1").style.background = "#ffda75";
    document.getElementById("mon2").style.background = "#ffde85";
    document.getElementById("mon3").style.background = "#ffda75";
    document.getElementById("mon4").style.background = "#ffde85";
    document.getElementById("mon5").style.background = "#ffda75";
    
    rowid = "mon" + selectrow
    iconid = "icon" + selectrow
    unitinfo = units[unitid]
    document.getElementById("icon" + selectrow).style.backgroundImage = unitinfo[21];
    document.getElementById("icon" + selectrow).style.backgroundSize="48px 48px";
    document.getElementById("name" + selectrow).innerHTML = unitinfo[0];
    
    getresistance(document.getElementById("frizz"+selectrow), unitinfo[1]);
    getresistance(document.getElementById("sizz"+selectrow), unitinfo[2]);
    getresistance(document.getElementById("crack"+selectrow), unitinfo[3]);
    getresistance(document.getElementById("woosh"+selectrow), unitinfo[4]);
    getresistance(document.getElementById("bang"+selectrow), unitinfo[5]);
    getresistance(document.getElementById("zap"+selectrow), unitinfo[6]);
    getresistance(document.getElementById("zam"+selectrow), unitinfo[7]);
    getresistance(document.getElementById("sleep"+selectrow), unitinfo[8]);
    getresistance(document.getElementById("poison"+selectrow), unitinfo[9]);
    getresistance(document.getElementById("plock"+selectrow), unitinfo[10]);
    getresistance(document.getElementById("slock"+selectrow), unitinfo[11]);
    getresistance(document.getElementById("mlock"+selectrow), unitinfo[12]);
    getresistance(document.getElementById("block"+selectrow), unitinfo[13]);
    getresistance(document.getElementById("hobble"+selectrow), unitinfo[14]);
    getresistance(document.getElementById("stun"+selectrow), unitinfo[15]);
    getresistance(document.getElementById("blind"+selectrow), unitinfo[16]);
    getresistance(document.getElementById("curse"+selectrow), unitinfo[17]);
    getresistance(document.getElementById("paralysis"+selectrow), unitinfo[18]);
    getresistance(document.getElementById("confusion"+selectrow), unitinfo[19]);
    getresistance(document.getElementById("charm"+selectrow), unitinfo[20]);
    
    // document.getElementById("frizz"+selectrow).innerHTML = unitinfo[1];
    
    selectrow = selectrow + 1
    if (selectrow === 6) {
        selectrow = 1
    }
    newrowid = "mon" + selectrow
    document.getElementById(newrowid).style.background = "#FCAA00";
}

var units = [
    // S Ranks
    ["Archdemon",               2,1,2,3,1,3,2,2,2,1,2,3,2,1,2,2,3,2,0,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_3_i.png')"],
    ["Baramos",                 3,2,3,1,2,2,1,2,3,2,2,2,2,2,2,1,3,2,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools/dq-tact/gacha/monster_147_i.png')"],
    ["Dragonlord",              2,3,3,1,2,1,2,1,2,2,1,2,2,3,3,2,2,0,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_128_i.png')"],
    ["DL True Form",            2,3,3,1,2,1,2,0,2,2,3,2,1,2,2,2,2,2,3,1,"url('https://img.altema.jp/dqtact/monster/icon/134.jpg')"],
    ["Emperor Slime",           2,1,1,3,2,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_89_i.png')"],
    ["Great Dragon",            1,1,2,3,2,3,2,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_2_i.png')"],
    ["Great Troll",             2,3,3,1,2,1,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_94_i.png')"],
    ["Hell Gladiator",          3,3,2,2,1,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_95_i.png')"],
    ["Hybird",                  1,2,3,1,3,2,2,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_91_i.png')"],
    ["Killer Machine",          1,2,2,2,3,3,1,1,0,2,2,1,2,3,2,2,2,2,3,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_83_i.png')"],
    ["K She-Slime",             1,2,2,2,3,3,1,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_1_i.png')"],
    ["Metal Dragon",            3,2,1,2,1,2,3,1,0,2,2,1,2,3,2,2,2,2,3,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_93_i.png')"],
    ["Night Clubber",           1,1,2,3,2,3,2,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_92_i.png')"],
    ["Prism Peacock",           1,2,2,1,3,2,3,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_5_i.png')"],
    ["Queen Slime",             2,1,2,3,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_139_i.png')"],
    ["Royal Reptile",           2,1,1,3,2,2,3,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_84_i.png')"],
    ["Slionheart",              3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_143_i.png')"],
    ["Squidzilla",              1,1,2,3,2,3,2,2,2,1,2,2,3,2,3,0,2,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_90_i.png')"],
    ["Wight King",              3,3,2,2,1,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_4_i.png')"],
    ["Zoma",                    1,2,2,3,1,3,2,1,2,2,1,2,2,3,0,2,2,3,2,2,"url('https://img.altema.jp/dqtact/monster/icon/158.jpg')"],
    // A Ranks
    ["Armful",                  3,2,2,1,3,2,1,1,1,2,2,2,2,3,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/149.jpg')"],
    ["Axesaurus",               2,2,3,1,3,2,1,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_97_i.png')"],
    ["Bone Baron",              3,3,2,2,1,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_12_i.png')"],
    ["Boreal Serpent",          3,2,1,2,1,2,3,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://img.altema.jp/dqtact/monster/icon/151.jpg')"],
    ["Boss Troll",              2,2,3,1,3,2,1,2,2,1,2,2,2,2,1,2,3,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/160.jpg')"],
    ["Cosmic Chimaera",         2,1,3,1,2,2,3,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_129_i.png')"],
    ["Dark Skeleton",           2,2,2,1,3,3,1,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_134_i.png')"],
    ["Devilmoth",               3,3,2,2,1,1,2,2,2,3,1,2,2,1,2,2,2,3,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_8_i.png')"],
    ["Dragon Slime",            3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_140_i.png')"],
    ["Dragon Zombie",           3,3,2,1,2,1,2,1,1,2,2,3,2,2,2,3,2,2,0,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_101_i.png')"],
    ["Gigantes",                1,2,2,2,3,3,1,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_100_i.png')"],
    ["Green Dragon",            2,2,3,1,3,2,1,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_14_i.png')"],
    ["Handsome Crab",           3,2,1,2,1,2,3,2,2,1,2,2,3,3,0,2,2,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_99_i.png')"],
    ["Hellion",                 2,2,3,1,3,2,1,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_85_i.png')"],
    ["King Bubble Slime",       1,1,2,3,2,3,2,3,0,2,3,2,2,2,2,2,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_141_i.png')"],
    ["King Slime",              3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_145_i.png')"],
    ["Lethal Armour",           1,2,2,2,3,3,1,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_10_i.png')"],
    ["Lime Slime",              3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_144_i.png')"],
    ["Living Statue",           2,1,1,3,2,2,3,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_9_i.png')"],
    ["Moosifer",                1,1,2,3,2,3,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_13_i.png')"],
    ["Pickled Slime",           3,3,2,2,1,1,2,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_138_i.png')"],
    ["Silvapithecus",           2,1,1,3,2,2,3,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_11_i.png')"],
    ["Slimecicle",              2,2,1,2,3,3,1,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_6_i.png')"],
    ["Slimeshroom",             2,3,3,1,2,1,2,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_96_i.png')"],
    ["Striking Sabrecat",       2,3,3,1,2,1,2,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_7_i.png')"],
    ["Umbra",                   2,1,1,2,3,3,2,2,1,2,3,2,2,2,2,2,2,0,2,3,"url('https://img.altema.jp/dqtact/monster/icon/159.jpg')"],
    ["Wyrtoise",                3,3,2,2,1,1,2,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_98_i.png')"],
// B Ranks
    ["Bad Karmour",             1,2,2,2,3,3,1,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://img.altema.jp/dqtact/monster/icon/23.jpg')"],
    ["Beleth",                  2,2,3,1,3,2,1,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/118.jpg')"],
    ["Cyber Slime",             3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_15_i.png')"],
    ["Dragurn",                 2,2,3,1,3,2,1,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_17_i.png')"],
    ["Drake Slime",             2,1,3,1,3,2,2,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/143.jpg')"],
    ["Drohl Drone",             1,2,2,2,3,3,1,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/78.jpg')"],
    ["Gargoyle",                3,2,1,2,1,2,3,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/19.jpg')"],
    ["Great Sabrecat",          3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/93.jpg')"],
    ["Hades Condor",            2,3,3,1,2,1,2,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_19_i.png')"],
    ["Knight Aberrant",         2,3,2,1,3,1,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_25_i.png')"],
    ["Lemon Slime",             1,2,2,2,3,3,1,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/16.jpg')"],
    ["Medislime",               3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/81.jpg')"],
    ["Orc Chieftain",           2,1,1,3,2,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/20.jpg')"],
    ["Raving Lunatick",         3,2,1,2,1,2,3,2,2,3,1,2,2,1,2,2,2,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/80.jpg')"],
    ["Robbin Oodlum",           3,2,1,2,1,2,3,2,3,2,2,2,2,1,0,1,2,2,2,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_133_i.png')"],
    ["Silhouette",              1,2,2,2,3,3,1,2,1,2,3,1,2,2,2,2,2,0,2,3,"url('https://img.altema.jp/dqtact/monster/icon/156.jpg')"],
    ["Skelegon",                2,2,2,1,3,3,1,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/119.jpg')"],
    ["Skeleton Soldier",        3,2,1,3,2,2,1,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/79.jpg')"],
    ["Stone Golem",             1,1,2,3,2,3,2,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_23_i.png')"],
    ["Tearwolf",                3,3,2,2,1,1,2,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/21.jpg')"],
    ["Tuskateer",               1,1,3,2,2,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/126.jpg')"],
    ["Whackolyte",              1,1,2,3,2,3,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/94.jpg')"],
    ["Wharfhorse",              1,2,2,2,3,3,1,2,2,1,2,2,3,2,3,0,2,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_18_i.png')"],
    ["Wyrtle",                  3,2,1,2,1,2,3,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://img.altema.jp/dqtact/monster/icon/153.jpg')"],
// C Ranks
    ["Angel Slime",             2,1,1,3,2,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_26_i.png')"],
    ["Bodkin Fletcher",         1,2,2,2,3,3,1,1,2,2,2,3,2,2,2,2,0,3,1,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_37_i.png')"],
    ["Buffalo Wing",            3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_33_i.png')"],
    ["Clawcerer",               2,2,3,1,3,2,1,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_32_i.png')"],
    ["Corpse Corporal",         3,3,2,1,2,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/113.jpg')"],
    ["Drackyma",                1,1,2,3,2,3,2,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/112.jpg')"],
    ["Fightgeist",              2,3,3,1,2,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/39.jpg')"],
    ["Goodybag",                1,2,2,2,3,3,1,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://img.altema.jp/dqtact/monster/icon/115.jpg')"],
    ["Grim Keeper",             3,3,2,2,1,2,1,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/105.jpg')"],
    ["Hocus Chimaera",          2,1,1,3,2,2,3,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/116.jpg')"],
    ["Hunter Mech",             2,1,1,3,2,2,3,1,0,2,2,1,2,3,2,2,2,2,3,2,"url('https://img.altema.jp/dqtact/monster/icon/104.jpg')"],
    ["Freezing Fog",            3,2,1,2,2,3,1,2,1,2,3,1,2,2,2,2,2,0,2,3,"url('https://img.altema.jp/dqtact/monster/icon/157.jpg')"],
    ["Jargon",                  2,3,3,1,2,1,2,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://img.altema.jp/dqtact/monster/icon/62.jpg')"],
    ["Knight Errant",           2,3,3,1,2,1,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/128.jpg')"],
    ["Lips",                    3,2,1,2,1,2,3,0,2,1,2,2,2,2,3,2,3,2,1,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_30_i.png')"],
    ["Man o War",               3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/27.jpg')"],
    ["Mandrake Mercenary",      1,1,2,3,2,3,2,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://img.altema.jp/dqtact/monster/icon/28.jpg')"],
    ["Metal Slime Knight",      1,1,2,3,2,3,2,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/99.jpg')"],
    ["Minidemon",               1,1,2,3,2,3,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_36_i.png')"],
    ["Mud Mannequin",           2,1,1,3,2,2,3,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_34_i.png')"],
    ["Mummy Boy",               3,3,2,2,1,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_38_i.png')"],
    ["Mushroom Mage",           3,2,1,2,3,2,1,0,2,1,2,2,2,2,3,2,3,2,1,2,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_31_i.png')"],
    ["Phantom Fencer",          3,3,1,2,1,2,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/117.jpg')"],
    ["Restless Armour",         1,1,2,3,2,3,2,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://img.altema.jp/dqtact/monster/icon/120.jpg')"],
    ["Salamander Fry",          2,2,3,1,3,2,1,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://img.altema.jp/dqtact/monster/icon/29.jpg')"],
    ["Scarewolf",               3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/102.jpg')"],
    ["Seaslime",                2,2,1,3,1,3,2,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/154.jpg')"],
    ["Shadow",                  2,3,3,1,2,1,2,2,1,2,3,1,2,2,2,2,2,0,2,3,"url('https://s3.ap-northeast-1.amazonaws.com/gamewith/article_tools%2Fdq-tact%2Fgacha%2Fmonster_35_i.png')"],
    ["Tigercub",                2,2,3,1,3,2,1,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/129.jpg')"],
// D Ranks
    ["Arrghgoyle",              2,2,3,1,3,2,1,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://img.altema.jp/dqtact/monster/icon/108.jpg')"],
    ["Bag o Laughs",            1,1,2,3,2,3,2,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://img.altema.jp/dqtact/monster/icon/84.jpg')"],
    ["Bewarewolf",              3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/95.jpg')"],
    ["Cannibox",                2,1,1,3,2,2,3,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://img.altema.jp/dqtact/monster/icon/43.jpg')"],
    ["Chimaera",                2,2,3,1,3,2,1,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/110.jpg')"],
    ["Crabid",                  1,2,2,2,3,3,1,2,2,1,2,2,3,2,3,0,2,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/101.jpg')"],
    ["Crack-billed Platypunk",  1,1,2,3,2,3,2,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/82.jpg')"],
    ["Dancing Flame",           1,2,3,1,3,2,2,2,1,2,3,1,2,2,2,2,2,0,2,3,"url('https://img.altema.jp/dqtact/monster/icon/121.jpg')"],
    ["Drackolyte",              1,2,2,2,3,3,1,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/83.jpg')"],
    ["Drooling Ghoul",          3,3,2,2,1,1,2,1,2,2,2,3,2,2,2,2,0,3,1,2,"url('https://img.altema.jp/dqtact/monster/icon/46.jpg')"],
    ["Golem",                   2,1,1,3,2,2,3,3,0,2,2,1,2,3,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/42.jpg')"],
    ["Great Sabrecub",          3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/41.jpg')"],
    ["Hawk Man",                3,2,1,2,1,2,3,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/45.jpg')"],
    ["Hell Nino",               1,1,3,2,3,2,2,2,1,2,3,1,2,2,2,2,2,0,2,3,"url('https://img.altema.jp/dqtact/monster/icon/123.jpg')"],
    ["Imp",                     1,1,2,3,2,3,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/109.jpg')"],
    ["Killing Machine Light",   2,2,3,1,3,2,1,1,0,2,2,1,2,3,2,2,2,2,3,2,"url('https://img.altema.jp/dqtact/monster/icon/106.jpg')"],
    ["Mad Mole",                3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/127.jpg')"],
    ["Mandrake Major",          3,2,1,2,1,2,3,2,3,2,2,2,1,2,2,2,2,1,0,3,"url('https://img.altema.jp/dqtact/monster/icon/125.jpg')"],
    ["Muddy Hand",              1,2,2,2,3,3,1,2,0,2,2,1,2,3,2,2,2,1,3,2,"url('https://img.altema.jp/dqtact/monster/icon/96.jpg')"],
    ["Orc",                     3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/107.jpg')"],
    ["Shell Slime",             1,1,2,3,2,3,2,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/44.jpg')"],
    ["Slime Knight",            1,2,1,2,2,3,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/40.jpg')"],
    ["Walking Corpse",          2,3,1,2,3,2,1,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/47.jpg')"],
// E Ranks
    ["Bodkin Archer",           1,2,2,2,3,3,1,1,2,2,2,3,2,2,2,2,0,3,1,2,"url('https://img.altema.jp/dqtact/monster/icon/53.jpg')"],
    ["Brownie",                 2,2,3,1,3,2,1,1,2,2,2,3,2,2,2,2,0,3,1,2,"url('https://img.altema.jp/dqtact/monster/icon/55.jpg')"],
    ["Bubble Slime",            1,2,2,2,3,3,1,3,0,2,3,2,2,2,2,2,1,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/114.jpg')"],
    ["Bullfinch",               2,2,3,1,3,2,1,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/85.jpg')"],
    ["Cactiball",               2,3,3,1,2,1,2,0,2,1,2,2,2,2,3,2,3,2,1,2,"url('https://img.altema.jp/dqtact/monster/icon/97.jpg')"],
    ["Carnivine",               3,2,1,2,1,2,3,0,2,1,2,2,2,2,3,2,3,2,1,2,"url('https://img.altema.jp/dqtact/monster/icon/124.jpg')"],
    ["Drackmage",               3,2,1,2,3,2,1,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/90.jpg')"],
    ["Firespirit",              1,2,3,1,3,2,2,2,1,2,3,1,2,2,2,2,2,0,2,3,"url('https://img.altema.jp/dqtact/monster/icon/122.jpg')"],
    ["Funghoul",                3,2,1,2,3,2,1,0,2,1,2,2,2,2,3,2,3,2,1,2,"url('https://img.altema.jp/dqtact/monster/icon/54.jpg')"],
    ["Healslime",               3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/51.jpg')"],
    ["Jailcat",                 1,2,2,2,3,3,1,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/88.jpg')"],
    ["Leery Lout",              2,1,1,3,2,2,3,1,2,2,2,3,2,2,2,2,0,3,1,2,"url('https://img.altema.jp/dqtact/monster/icon/63.jpg')"],
    ["Lickspittle",             2,3,3,1,2,1,2,1,2,2,2,3,2,2,2,2,0,3,1,2,"url('https://img.altema.jp/dqtact/monster/icon/49.jpg')"],
    ["Mecha-Mynah",             1,1,2,3,2,3,2,1,0,2,2,1,2,3,2,2,2,2,3,2,"url('https://img.altema.jp/dqtact/monster/icon/52.jpg')"],
    ["Meowgician",              2,2,3,1,3,2,1,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/86.jpg')"],
    ["She-Slime",               2,1,1,3,2,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/89.jpg')"],
    ["Skeleton",                3,3,2,2,1,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/48.jpg')"],
    ["Spiked Hare",             2,3,3,1,2,1,2,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/155.jpg')"],
    ["Stump Chump",             3,2,1,2,1,2,3,0,2,1,2,2,2,2,3,2,3,2,1,2,"url('https://img.altema.jp/dqtact/monster/icon/87.jpg')"],
    ["Teeny Sanguini",          3,3,2,2,1,1,2,2,2,2,1,2,3,2,1,2,2,3,2,0,"url('https://img.altema.jp/dqtact/monster/icon/50.jpg')"],
// F Ranks
    ["Bunicorn",                3,2,1,3,1,2,2,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/56.jpg')"],
    ["Candy Cat",               2,2,3,1,3,2,1,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/58.jpg')"],
    ["Dracky",                  2,2,3,1,3,2,1,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/57.jpg')"],
    ["Ghost",                   2,3,3,1,2,1,2,1,1,2,2,3,2,2,2,3,2,0,2,2,"url('https://img.altema.jp/dqtact/monster/icon/59.jpg')"],
    ["Hammerhood",              2,2,3,1,3,2,1,1,2,2,2,3,2,2,2,2,0,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/111.jpg')"],
    ["Mischievous Mole",        1,1,2,3,2,3,2,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/98.jpg')"],
    ["Platypunk",               3,2,1,2,1,2,3,3,2,3,2,2,2,1,0,1,2,2,2,2,"url('https://img.altema.jp/dqtact/monster/icon/92.jpg')"],
    ["Slime",                   3,2,1,2,1,2,3,3,2,2,3,2,2,2,2,0,1,2,2,1,"url('https://img.altema.jp/dqtact/monster/icon/91.jpg')"],
    ["Stark Raven",             1,2,2,2,3,3,1,3,3,2,2,2,1,0,2,2,2,1,2,2,"url('https://img.altema.jp/dqtact/monster/icon/152.jpg')"],
];
