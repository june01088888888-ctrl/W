import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="승준의 어드벤처",
    page_icon="⚔️",
    layout="wide"
)

game = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #101827;
    font-family: Arial, sans-serif;
}

#game {
    position: relative;
    width: 100%;
    max-width: 1100px;
    height: 600px;
    margin: auto;
    overflow: hidden;
    background: linear-gradient(#4db8ff 0%, #9cddff 65%, #72c75b 65%);
    border: 5px solid #17243a;
    border-radius: 15px;
}

/* 구름 */
.cloud {
    position: absolute;
    font-size: 55px;
}

/* 땅 */
#ground {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 75px;
    background: #684126;
    border-top: 12px solid #4caf3d;
}

/* 캐릭터 */
#player {
    position: absolute;
    left: 100px;
    bottom: 75px;
    width: 55px;
    height: 70px;
    font-size: 52px;
    z-index: 10;
}

/* 코인 */
.coin {
    position: absolute;
    font-size: 35px;
    z-index: 5;
}

/* 적 */
.enemy {
    position: absolute;
    font-size: 45px;
    z-index: 6;
}

/* 플랫폼 */
.platform {
    position: absolute;
    height: 25px;
    background: #654225;
    border-top: 9px solid #4caf3d;
    border-radius: 5px;
}

/* HUD */
#hud {
    position: absolute;
    top: 15px;
    left: 15px;
    right: 15px;
    padding: 12px 25px;
    display: flex;
    justify-content: space-between;
    color: white;
    background: rgba(15,25,45,.85);
    border-radius: 12px;
    font-size: 21px;
    font-weight: bold;
    z-index: 30;
}

/* 공격 이펙트 */
#attack {
    position: absolute;
    display: none;
    font-size: 45px;
    z-index: 20;
}

/* 게임 메시지 */
#message {
    display: none;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    padding: 30px 50px;
    color: white;
    background: rgba(0,0,0,.9);
    border-radius: 20px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    z-index: 100;
}

/* 조작 */
#controls {
    max-width: 1100px;
    margin: 12px auto;
    padding: 12px;
    text-align: center;
    color: white;
    background: #17243a;
    border-radius: 10px;
    font-size: 18px;
}
</style>
</head>

<body>

<div id="game">

    <div id="hud">
        <span>❤️ 체력: <b id="hp">3</b></span>
        <span>🪙 코인: <b id="score">0</b></span>
        <span>💀 처치: <b id="kills">0</b></span>
    </div>

    <div class="cloud" style="left:120px; top:100px;">☁️</div>
    <div class="cloud" style="left:650px; top:130px;">☁️</div>
    <div class="cloud" style="left:900px; top:80px;">☁️</div>

    <div id="player">🧙</div>
    <div id="attack">⚔️</div>

    <!-- 코인 -->
    <div class="coin" style="left:300px; bottom:150px;">🪙</div>
    <div class="coin" style="left:450px; bottom:250px;">🪙</div>
    <div class="coin" style="left:600px; bottom:150px;">🪙</div>
    <div class="coin" style="left:760px; bottom:250px;">🪙</div>
    <div class="coin" style="left:930px; bottom:150px;">🪙</div>

    <!-- 적 -->
    <div class="enemy" style="left:520px; bottom:75px;">👾</div>
    <div class="enemy" style="left:850px; bottom:75px;">💀</div>

    <!-- 플랫폼 -->
    <div class="platform"
         style="left:230px; bottom:130px; width:170px;"></div>

    <div class="platform"
         style="left:420px; bottom:230px; width:170px;"></div>

    <div class="platform"
         style="left:700px; bottom:130px; width:170px;"></div>

    <div id="ground"></div>

    <div id="message"></div>

</div>

<div id="controls">
    ⬅️ ➡️ 이동 &nbsp;&nbsp; ⬆️ 점프 &nbsp;&nbsp; SPACE 공격
</div>

<script>

const player = document.getElementById("player");
const attack = document.getElementById("attack");
const game = document.getElementById("game");

let x = 100;
let y = 75;

let vx = 0;
let vy = 0;

let hp = 3;
let score = 0;
let kills = 0;

let jumping = false;
let attacking = false;
let invincible = false;

const keys = {};

document.addEventListener("keydown", function(e) {

    keys[e.key] = true;

    if (e.key === "ArrowUp" && !jumping) {
        vy = 15;
        jumping = true;
    }

    if (e.key === " ") {
        e.preventDefault();
        doAttack();
    }
});

document.addEventListener("keyup", function(e) {
    keys[e.key] = false;
});


function doAttack() {

    if (attacking) return;

    attacking = true;

    attack.style.display = "block";
    attack.style.left = (x + 45) + "px";
    attack.style.bottom = (y + 10) + "px";

    player.innerHTML = "⚔️";

    setTimeout(function() {

        document.querySelectorAll(".enemy").forEach(enemy => {

            if (enemy.style.display === "none")
                return;

            const ex = parseInt(enemy.style.left);
            const ey = parseInt(enemy.style.bottom);

            if (
                Math.abs(x - ex) < 100 &&
                Math.abs(y - ey) < 100
            ) {

                enemy.style.display = "none";

                kills++;
                score += 100;

                document.getElementById("kills").innerText = kills;
                document.getElementById("score").innerText = score;
            }

        });

    }, 100);

    setTimeout(function() {

        attack.style.display = "none";
        player.innerHTML = "🧙";
        attacking = false;

    }, 250);
}


function collectCoins() {

    document.querySelectorAll(".coin").forEach(coin => {

        if (coin.style.display === "none")
            return;

        const cx = parseInt(coin.style.left);
        const cy = parseInt(coin.style.bottom);

        if (
            Math.abs(x - cx) < 50 &&
            Math.abs(y - cy) < 60
        ) {

            coin.style.display = "none";

            score += 50;

            document.getElementById("score").innerText = score;
        }
    });
}


function enemyCollision() {

    if (invincible)
        return;

    document.querySelectorAll(".enemy").forEach(enemy => {

        if (enemy.style.display === "none")
            return;

        const ex = parseInt(enemy.style.left);
        const ey = parseInt(enemy.style.bottom);

        if (
            Math.abs(x - ex) < 45 &&
            Math.abs(y - ey) < 60
        ) {

            hp--;

            document.getElementById("hp").innerText = hp;

            x -= 80;

            invincible = true;

            setTimeout(() => {
                invincible = false;
            }, 1000);

            if (hp <= 0) {
                gameOver();
            }
        }
    });
}


function gameOver() {

    document.getElementById("message").innerHTML =
        "💀 GAME OVER<br><br>" +
        "<small>새로고침해서 다시 플레이하세요!</small>";

    document.getElementById("message").style.display = "block";
}


function update() {

    if (keys["ArrowLeft"]) {

        vx = -6;
        player.style.transform = "scaleX(-1)";
    }

    else if (keys["ArrowRight"]) {

        vx = 6;
        player.style.transform = "scaleX(1)";
    }

    else {

        vx *= 0.8;
    }


    x += vx;


    // 중력
    vy -= 0.7;
    y += vy;


    // 바닥
    if (y <= 75) {

        y = 75;
        vy = 0;
        jumping = false;
    }


    // 화면 밖 방지
    if (x < 0)
        x = 0;

    if (x > game.clientWidth - 60)
        x = game.clientWidth - 60;


    player.style.left = x + "px";
    player.style.bottom = y + "px";


    collectCoins();
    enemyCollision();


    // 코인을 전부 먹으면 승리
    if (
        document.querySelectorAll(".coin:not([style*='display: none'])").length === 0
    ) {

        document.getElementById("message").innerHTML =
            "🏆 스테이지 클리어!<br><br>" +
            "점수: " + score;

        document.getElementById("message").style.display = "block";
    }


    requestAnimationFrame(update);
}

update();

</script>

</body>
</html>
"""

components.html(
    game,
    height=680,
    scrolling=False
)
