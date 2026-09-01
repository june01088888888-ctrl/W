import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="승준의 어드벤처", page_icon="⚔️")

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
}

body {
    margin: 0;
    background: #101827;
    font-family: Arial, sans-serif;
}

#game {
    position: relative;
    width: 100%;
    height: 500px;
    overflow: hidden;
    background: linear-gradient(#4db8ff 0%, #9cddff 58%, #78c850 58%);
    border: 4px solid #17243a;
    border-radius: 15px;
}

#ground {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 65px;
    background: #70452a;
    border-top: 10px solid #4caf3d;
}

#player {
    position: absolute;
    left: 50px;
    bottom: 65px;
    font-size: 48px;
    z-index: 10;
}

.coin {
    position: absolute;
    font-size: 30px;
}

.enemy {
    position: absolute;
    font-size: 40px;
}

.platform {
    position: absolute;
    height: 20px;
    background: #70452a;
    border-top: 8px solid #4caf3d;
}

#hud {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    height: 50px;
    padding: 10px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    color: white;
    background: rgba(0,0,0,.7);
    border-radius: 12px;
    z-index: 20;
    font-weight: bold;
}

#start {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,.75);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    z-index: 50;
}

#start button {
    padding: 15px 40px;
    font-size: 22px;
    border: 0;
    border-radius: 15px;
    background: #2878ff;
    color: white;
    font-weight: bold;
}

#message {
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,.8);
    color: white;
    text-align: center;
    padding-top: 170px;
    font-size: 28px;
    z-index: 40;
}

#controls {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

button.control {
    width: 70px;
    height: 65px;
    margin: 3px;
    border: 0;
    border-radius: 16px;
    background: #263752;
    color: white;
    font-size: 28px;
    touch-action: none;
}

button.attack {
    background: #a82d35;
}

button.jump {
    background: #2878ff;
}
</style>
</head>

<body>

<div id="game">

<div id="hud">
<span>❤️ <b id="hp">3</b></span>
<span>🪙 <b id="score">0</b></span>
<span>💀 <b id="kills">0</b></span>
</div>

<div id="player">🧙</div>

<div class="coin" style="left:25%;bottom:140px">🪙</div>
<div class="coin" style="left:43%;bottom:220px">🪙</div>
<div class="coin" style="left:60%;bottom:140px">🪙</div>
<div class="coin" style="left:76%;bottom:220px">🪙</div>
<div class="coin" style="left:90%;bottom:140px">🪙</div>

<div class="enemy" style="left:50%;bottom:65px">👾</div>
<div class="enemy" style="left:82%;bottom:65px">💀</div>

<div class="platform" style="left:20%;bottom:115px;width:140px"></div>
<div class="platform" style="left:40%;bottom:195px;width:140px"></div>
<div class="platform" style="left:70%;bottom:115px;width:140px"></div>

<div id="ground"></div>

<div id="start">
<h1>⚔️ 승준의 어드벤처</h1>
<p>코인을 모두 모으세요!</p>
<button id="startButton">🎮 게임 시작</button>
</div>

<div id="message"></div>

</div>

<div id="controls">

<div>
<button class="control" id="left">⬅️</button>
<button class="control" id="right">➡️</button>
</div>

<div>
<button class="control jump" id="jump">⬆️</button>
<button class="control attack" id="attack">⚔️</button>
</div>

</div>

<script>

const player = document.getElementById("player");
const game = document.getElementById("game");

let x = 50;
let y = 65;
let vx = 0;
let vy = 0;

let hp = 3;
let score = 0;
let kills = 0;

let playing = false;
let jumping = false;
let attacking = false;

let leftPressed = false;
let rightPressed = false;
let invincible = false;


document.getElementById("startButton").onclick = function() {

    document.getElementById("start").style.display = "none";

    playing = true;

    requestAnimationFrame(update);
};


function buttonHold(id, start, end) {

    const b = document.getElementById(id);

    b.addEventListener("touchstart", function(e) {
        e.preventDefault();
        start();
    }, {passive:false});

    b.addEventListener("touchend", function(e) {
        e.preventDefault();
        end();
    }, {passive:false});

    b.addEventListener("mousedown", start);
    b.addEventListener("mouseup", end);
}


buttonHold(
    "left",
    function(){ leftPressed = true; },
    function(){ leftPressed = false; }
);

buttonHold(
    "right",
    function(){ rightPressed = true; },
    function(){ rightPressed = false; }
);


function jump() {

    if (!playing) return;

    if (!jumping) {

        vy = 14;
        jumping = true;
    }
}


document.getElementById("jump").onclick = jump;


function attack() {

    if (!playing || attacking) return;

    attacking = true;

    player.innerHTML = "⚔️";

    setTimeout(function(){

        document.querySelectorAll(".enemy").forEach(function(enemy){

            if(enemy.style.display === "none") return;

            let ex = parseFloat(enemy.style.left);
            let ey = parseFloat(enemy.style.bottom);

            if(
                Math.abs(x-ex) < 100 &&
                Math.abs(y-ey) < 90
            ){

                enemy.style.display = "none";

                kills++;
                score += 100;

                document.getElementById("kills").innerText = kills;
                document.getElementById("score").innerText = score;
            }

        });

    },100);


    setTimeout(function(){

        player.innerHTML = "🧙";
        attacking = false;

    },300);
}


document.getElementById("attack").onclick = attack;


function collectCoins() {

    document.querySelectorAll(".coin").forEach(function(coin){

        if(coin.style.display === "none") return;

        let cx = parseFloat(coin.style.left);
        let cy = parseFloat(coin.style.bottom);

        if(
            Math.abs(x-cx) < 45 &&
            Math.abs(y-cy) < 55
        ){

            coin.style.display = "none";

            score += 50;

            document.getElementById("score").innerText = score;
        }

    });
}


function hitEnemy() {

    if(invincible) return;

    document.querySelectorAll(".enemy").forEach(function(enemy){

        if(enemy.style.display === "none") return;

        let ex = parseFloat(enemy.style.left);
        let ey = parseFloat(enemy.style.bottom);

        if(
            Math.abs(x-ex) < 40 &&
            Math.abs(y-ey) < 50
        ){

            hp--;

            document.getElementById("hp").innerText = hp;

            x -= 60;

            invincible = true;

            setTimeout(function(){
                invincible = false;
            },1000);

            if(hp <= 0){

                playing = false;

                document.getElementById("message").innerHTML =
                    "💀 GAME OVER<br><br>" +
                    "<button onclick='location.reload()'>" +
                    "🔄 다시하기</button>";

                document.getElementById("message").style.display = "block";
            }
        }

    });
}


function checkWin() {

    let coins = document.querySelectorAll(".coin");

    let remaining = 0;

    coins.forEach(function(c){

        if(c.style.display !== "none")
            remaining++;
    });

    if(remaining === 0){

        playing = false;

        document.getElementById("message").innerHTML =
            "🏆 클리어!<br><br>" +
            "점수: " + score +
            "<br><br>" +
            "<button onclick='location.reload()'>" +
            "🔄 다시하기</button>";

        document.getElementById("message").style.display = "block";
    }
}


function update() {

    if(!playing) return;


    if(leftPressed){

        vx = -5;

        player.style.transform = "scaleX(-1)";
    }

    else if(rightPressed){

        vx = 5;

        player.style.transform = "scaleX(1)";
    }

    else{

        vx *= 0.8;
    }


    x += vx;


    vy -= 0.65;
    y += vy;


    if(y <= 65){

        y = 65;
        vy = 0;
        jumping = false;
    }


    if(x < 0)
        x = 0;

    if(x > game.clientWidth - 60)
        x = game.clientWidth - 60;


    player.style.left = x + "px";
    player.style.bottom = y + "px";


    collectCoins();
    hitEnemy();
    checkWin();


    requestAnimationFrame(update);
}


// 키보드도 지원
document.addEventListener("keydown", function(e){

    if(e.key === "ArrowLeft")
        leftPressed = true;

    if(e.key === "ArrowRight")
        rightPressed = true;

    if(e.key === "ArrowUp")
        jump();

    if(e.key === " ")
        attack();
});


document.addEventListener("keyup", function(e){

    if(e.key === "ArrowLeft")
        leftPressed = false;

    if(e.key === "ArrowRight")
        rightPressed = false;
});

</script>

</body>
</html>
"""

components.html(html, height=620, scrolling=False)
