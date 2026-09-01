```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="승준의 어드벤처",
    page_icon="⚔️",
    layout="centered"
)

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
}

body {
    margin: 0;
    background: #101827;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game {
    position: relative;
    width: 100%;
    height: 520px;
    overflow: hidden;
    background: linear-gradient(
        #4db8ff 0%,
        #9cddff 60%,
        #72c75b 60%,
        #72c75b 100%
    );
    border: 4px solid #17243a;
    border-radius: 15px;
}

/* 구름 */
.cloud {
    position: absolute;
    font-size: 45px;
}

/* 땅 */
#ground {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 70px;
    background: #684126;
    border-top: 12px solid #4caf3d;
}

/* 플레이어 */
#player {
    position: absolute;
    left: 50px;
    bottom: 70px;
    width: 55px;
    height: 65px;
    font-size: 48px;
    z-index: 10;
}

/* 코인 */
.coin {
    position: absolute;
    font-size: 32px;
    z-index: 5;
}

/* 적 */
.enemy {
    position: absolute;
    font-size: 42px;
    z-index: 6;
}

/* 플랫폼 */
.platform {
    position: absolute;
    height: 22px;
    background: #654225;
    border-top: 8px solid #4caf3d;
    border-radius: 5px;
}

/* HUD */
#hud {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    height: 55px;
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
    background: rgba(15,25,45,.88);
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    z-index: 30;
}

/* 시작 화면 */
#startScreen {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,.72);
    z-index: 100;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    text-align: center;
}

#startScreen h1 {
    font-size: 34px;
    margin: 10px;
}

#startScreen p {
    font-size: 16px;
}

#startButton {
    margin-top: 20px;
    padding: 16px 45px;
    border: 0;
    border-radius: 15px;
    background: #2878ff;
    color: white;
    font-size: 22px;
    font-weight: bold;
}

/* 게임 종료 */
#message {
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,.78);
    z-index: 90;
    color: white;
    text-align: center;
    padding-top: 180px;
    font-size: 28px;
    font-weight: bold;
}

/* 모바일 조작 */
#controls {
    width: 100%;
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.controlGroup {
    display: flex;
    gap: 8px;
}

.controlButton {
    width: 65px;
    height: 65px;
    border: none;
    border-radius: 18px;
    background: #263752;
    color: white;
    font-size: 28px;
    font-weight: bold;
    touch-action: none;
}

#attackButton {
    background: #a82d35;
}

#jumpButton {
    background: #2878ff;
}

.controlButton:active {
    transform: scale(.92);
}
</style>
</head>

<body>

<div id="game">

    <div id="hud">
        <span>❤️ <span id="hp">3</span></span>
        <span>🪙 <span id="score">0</span></span>
        <span>💀 <span id="kills">0</span></span>
    </div>

    <div class="cloud" style="left:80px;top:100px;">☁️</div>
    <div class="cloud" style="left:65%;top:130px;">☁️</div>

    <div id="player">🧙</div>

    <!-- 코인 -->
    <div class="coin" style="left:25%;bottom:150px;">🪙</div>
    <div class="coin" style="left:43%;bottom:235px;">🪙</div>
    <div class="coin" style="left:58%;bottom:150px;">🪙</div>
    <div class="coin" style="left:73%;bottom:235px;">🪙</div>
    <div class="coin" style="left:88%;bottom:150px;">🪙</div>

    <!-- 적 -->
    <div class="enemy" style="left:48%;bottom:70px;">👾</div>
    <div class="enemy" style="left:80%;bottom:70px;">💀</div>

    <!-- 플랫폼 -->
    <div class="platform"
         style="left:20%;bottom:125px;width:150px;"></div>

    <div class="platform"
         style="left:40%;bottom:210px;width:150px;"></div>

    <div class="platform"
         style="left:68%;bottom:125px;width:150px;"></div>

    <div id="ground"></div>

    <!-- 시작 -->
    <div id="startScreen">
        <h1>⚔️ 승준의 어드벤처</h1>
        <p>코인을 모으고 적을 물리치세요!</p>
        <button id="startButton">🎮 게임 시작</button>
    </div>

    <!-- 종료 -->
    <div id="message"></div>

</div>

<!-- 터치 조작 -->
<div id="controls">

    <div class="controlGroup">
        <button class="controlButton" id="leftButton">⬅️</button>
        <button class="controlButton" id="rightButton">➡️</button>
    </div>

    <div class="controlGroup">
        <button class="controlButton" id="jumpButton">⬆️</button>
        <button class="controlButton" id="attackButton">⚔️</button>
    </div>

</div>


<script>

const game = document.getElementById("game");
const player = document.getElementById("player");

let x = 50;
let y = 70;

let vx = 0;
let vy = 0;

let hp = 3;
let score = 0;
let kills = 0;

let playing = false;
let jumping = false;
let attacking = false;
let invincible = false;

let leftPressed = false;
let rightPressed = false;


// ==========================
// 시작 버튼
// ==========================

document.getElementById("startButton").addEventListener("click", startGame);

function startGame() {

    document.getElementById("startScreen").style.display = "none";

    playing = true;

    requestAnimationFrame(update);
}


// ==========================
// 터치 버튼
// ==========================

function holdButton(button, start, end) {

    button.addEventListener("touchstart", function(e) {
        e.preventDefault();
        start();
    }, {passive:false});

    button.addEventListener("touchend", function(e) {
        e.preventDefault();
        end();
    }, {passive:false});

    button.addEventListener("touchcancel", function(e) {
        e.preventDefault();
        end();
    }, {passive:false});

    // PC에서도 테스트 가능
    button.addEventListener("mousedown", function() {
        start();
    });

    button.addEventListener("mouseup", function() {
        end();
    });
}


holdButton(
    document.getElementById("leftButton"),
    () => leftPressed = true,
    () => leftPressed = false
);

holdButton(
    document.getElementById("rightButton"),
    () => rightPressed = true,
    () => rightPressed = false
);


// 점프
function jump() {

    if (!playing) return;

    if (!jumping) {
        vy = 14;
        jumping = true;
    }
}

document.getElementById("jumpButton")
.addEventListener("touchstart", function(e) {
    e.preventDefault();
    jump();
}, {passive:false});

document.getElementById("jumpButton")
.addEventListener("click", jump);


// 공격
function attack() {

    if (!playing || attacking) return;

    attacking = true;

    player.innerHTML = "⚔️";

    setTimeout(function() {

        document.querySelectorAll(".enemy").forEach(enemy => {

            if (enemy.style.display === "none")
                return;

            const ex = parseFloat(enemy.style.left);
            const ey = parseFloat(enemy.style.bottom);

            if (
                Math.abs(x - ex) < 100 &&
                Math.abs(y - ey) < 90
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

        player.innerHTML = "🧙";
        attacking = false;

    }, 300);
}

document.getElementById("attackButton")
.addEventListener("touchstart", function(e) {
    e.preventDefault();
    attack();
}, {passive:false});

document.getElementById("attackButton")
.addEventListener("click", attack);


// ==========================
// 키보드도 지원
// ==========================

document.addEventListener("keydown", function(e) {

    if (e.key === "ArrowLeft")
        leftPressed = true;

    if (e.key === "ArrowRight")
        rightPressed = true;

    if (e.key === "ArrowUp")
        jump();

    if (e.key === " ")
        attack();
});

document.addEventListener("keyup", function(e) {

    if (e.key === "ArrowLeft")
        leftPressed = false;

    if (e.key === "ArrowRight")
        rightPressed = false;
});


// ==========================
// 코인
// ==========================

function collectCoins() {

    document.querySelectorAll(".coin").forEach(coin => {

        if (coin.style.display === "none")
            return;

        const cx = parseFloat(coin.style.left);
        const cy = parseFloat(coin.style.bottom);

        if (
            Math.abs(x - cx) < 45 &&
            Math.abs(y - cy) < 55
        ) {

            coin.style.display = "none";

            score += 50;

            document.getElementById("score").innerText = score;
        }
    });
}


// ==========================
// 적 충돌
// ==========================

function enemyCollision() {

    if (invincible)
        return;

    document.querySelectorAll(".enemy").forEach(enemy => {

        if (enemy.style.display === "none")
            return;

        const ex = parseFloat(enemy.style.left);
        const ey = parseFloat(enemy.style.bottom);

        if (
            Math.abs(x - ex) < 40 &&
            Math.abs(y - ey) < 55
        ) {

            hp--;

            document.getElementById("hp").innerText = hp;

            x -= 70;

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


// ==========================
// 게임 오버
// ==========================

function gameOver() {

    playing = false;

    document.getElementById("message").innerHTML =
        "💀 GAME OVER<br><br>" +
        "<span style='font-size:18px'>점수: " +
        score +
        "</span><br><br>" +
        "<button onclick='location.reload()' " +
        "style='padding:14px 25px;border:0;border-radius:12px;font-size:18px'>" +
        "🔄 다시하기</button>";

    document.getElementById("message").style.display = "block";
}


// ==========================
// 승리
// ==========================

function checkWin() {

    const remaining =
        document.querySelectorAll(".coin:not([style*='display: none'])");

    if (remaining.length === 0) {

        playing = false;

        document.getElementById("message").innerHTML =
            "🏆 스테이지 클리어!<br><br>" +
            "<span style='font-size:18px'>점수: " +
            score +
            "</span><br><br>" +
            "<button onclick='location.reload()' " +
            "style='padding:14px 25px;border:0;border-radius:12px;font-size:18px'>" +
            "🔄 다시하기</button>";

        document.getElementById("message").style.display = "block";
    }
}


// ==========================
// 게임 루프
// ==========================

function update() {

    if (!playing)
        return;


    // 이동
    if (leftPressed) {

        vx = -5;

        player.style.transform = "scaleX(-1)";
    }

    else if (rightPressed) {

        vx = 5;

        player.style.transform = "scaleX(1)";
    }

    else {

        vx *= 0.8;
    }


    x += vx;


    // 중력
    vy -= 0.65;
    y += vy;


    // 바닥
    if (y <= 70) {

        y = 70;
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
    checkWin();


    requestAnimationFrame(update);
}

</script>

</body>
</html>
"""

components.html(
    html,
    height=620,
    scrolling=False
)
```
