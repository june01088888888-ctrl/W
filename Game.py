import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Brick Blast",
    page_icon="🧱",
    layout="centered"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }

    h1 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧱 BRICK BLAST")

html = r"""
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
    background:
        radial-gradient(circle at top, #172554, #020617 70%);
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#wrap {
    width: 100%;
    max-width: 800px;
    margin: auto;
}

#top {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: rgba(15,23,42,.9);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 8px;
    font-size: 15px;
}

.stat {
    text-align: center;
}

.value {
    font-size: 20px;
    font-weight: bold;
}

#game {
    display: block;
    width: 100%;
    max-width: 760px;
    height: auto;
    margin: auto;
    border-radius: 15px;
    border: 2px solid #475569;
    box-shadow: 0 0 30px rgba(59,130,246,.25);
    touch-action: none;
}

#buttons {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 9px;
}

button {
    border: none;
    border-radius: 9px;
    padding: 9px 16px;
    background: #2563eb;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #3b82f6;
}

#help {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 7px;
}
</style>
</head>

<body>

<div id="wrap">

<div id="top">

<div class="stat">
점수
<div class="value" id="score">0</div>
</div>

<div class="stat">
최고점
<div class="value" id="high">0</div>
</div>

<div class="stat">
레벨
<div class="value" id="level">1</div>
</div>

<div class="stat">
❤️
<div class="value" id="lives">3</div>
</div>

<div class="stat">
🔥 콤보
<div class="value" id="combo">0</div>
</div>

</div>

<canvas id="game" width="760" height="560"></canvas>

<div id="buttons">
<button onclick="startGame()">▶ 시작</button>
<button onclick="togglePause()">⏸ 일시정지</button>
<button onclick="restartGame()">🔄 재시작</button>
</div>

<div id="help">
마우스 / 손가락으로 패들을 움직이세요
</div>

</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

let score = 0;
let highScore = Number(localStorage.getItem("brickHigh") || 0);
let level = 1;
let lives = 3;
let combo = 0;

let running = false;
let paused = false;
let gameOver = false;
let victory = false;

let shake = 0;

let particles = [];
let powerups = [];

let paddle = {
    x: W / 2 - 60,
    y: H - 42,
    width: 120,
    height: 15,
    normalWidth: 120
};

let balls = [];

let bricks = [];

const colors = [
    "#ef4444",
    "#f97316",
    "#eab308",
    "#22c55e",
    "#06b6d4",
    "#3b82f6",
    "#8b5cf6"
];

function createBall(x, y, dx, dy) {

    return {
        x: x,
        y: y,
        r: 9,
        dx: dx,
        dy: dy,
        alive: true,
        trail: []
    };

}

function resetBalls() {

    balls = [
        createBall(
            W / 2,
            H - 65,
            4.2,
            -5
        )
    ];

}

function createLevel() {

    bricks = [];

    let rows = Math.min(5 + level, 9);
    let cols = 10;

    let bw = 63;
    let bh = 23;
    let gap = 8;

    let total =
        cols * bw +
        (cols - 1) * gap;

    let startX = (W - total) / 2;
    let startY = 55;

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            let type = "normal";

            let chance = Math.random();

            if (chance < 0.08 + level * 0.01) {
                type = "bomb";
            }
            else if (chance < 0.16 + level * 0.01) {
                type = "strong";
            }

            bricks.push({
                x: startX + c * (bw + gap),
                y: startY + r * (bh + gap),
                w: bw,
                h: bh,
                type: type,
                hp: type === "strong" ? 2 : 1,
                alive: true
            });

        }

    }

}

function updateUI() {

    document.getElementById("score").textContent = score;
    document.getElementById("high").textContent = highScore;
    document.getElementById("level").textContent = level;
    document.getElementById("lives").textContent = lives;
    document.getElementById("combo").textContent = combo;

}

function addScore(amount) {

    let multiplier =
        Math.min(1 + Math.floor(combo / 5), 5);

    score += amount * multiplier;

    if (score > highScore) {

        highScore = score;

        localStorage.setItem(
            "brickHigh",
            highScore
        );

    }

    updateUI();

}

function createParticles(x, y, color, count = 10) {

    for (let i = 0; i < count; i++) {

        let angle =
            Math.random() * Math.PI * 2;

        let speed =
            Math.random() * 4 + 1;

        particles.push({

            x: x,
            y: y,

            dx: Math.cos(angle) * speed,
            dy: Math.sin(angle) * speed,

            life: 35 + Math.random() * 25,

            color: color

        });

    }

}

function updateParticles() {

    for (let i = particles.length - 1; i >= 0; i--) {

        let p = particles[i];

        p.x += p.dx;
        p.y += p.dy;

        p.dy += 0.08;

        p.life--;

        if (p.life <= 0) {
            particles.splice(i, 1);
        }

    }

}

function drawParticles() {

    particles.forEach(p => {

        ctx.globalAlpha =
            Math.max(0, p.life / 50);

        ctx.fillStyle = p.color;

        ctx.fillRect(
            p.x,
            p.y,
            4,
            4
        );

    });

    ctx.globalAlpha = 1;

}

function drawBackground() {

    ctx.fillStyle = "#020617";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    // 별
    ctx.fillStyle = "#334155";

    for (let i = 0; i < 80; i++) {

        let x = (i * 97) % W;
        let y = (i * 53) % H;

        ctx.fillRect(
            x,
            y,
            1.5,
            1.5
        );

    }

}

function drawPaddle() {

    let gradient =
        ctx.createLinearGradient(
            paddle.x,
            paddle.y,
            paddle.x + paddle.width,
            paddle.y
        );

    gradient.addColorStop(
        0,
        "#06b6d4"
    );

    gradient.addColorStop(
        .5,
        "#3b82f6"
    );

    gradient.addColorStop(
        1,
        "#8b5cf6"
    );

    ctx.fillStyle = gradient;

    ctx.shadowBlur = 15;
    ctx.shadowColor = "#3b82f6";

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        8
    );

    ctx.fill();

    ctx.shadowBlur = 0;

}

function drawBalls() {

    balls.forEach(ball => {

        ball.trail.forEach((t, i) => {

            ctx.globalAlpha =
                i / ball.trail.length * .3;

            ctx.fillStyle = "#facc15";

            ctx.beginPath();

            ctx.arc(
                t.x,
                t.y,
                ball.r * (i / ball.trail.length),
                0,
                Math.PI * 2
            );

            ctx.fill();

        });

        ctx.globalAlpha = 1;

        ctx.shadowBlur = 20;
        ctx.shadowColor = "#facc15";

        ctx.fillStyle = "#fde047";

        ctx.beginPath();

        ctx.arc(
            ball.x,
            ball.y,
            ball.r,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.shadowBlur = 0;

    });

}

function drawBricks() {

    bricks.forEach(brick => {

        if (!brick.alive) return;

        let color;

        if (brick.type === "bomb") {

            color = "#dc2626";

        }
        else if (brick.type === "strong") {

            color = "#a855f7";

        }
        else {

            let row =
                Math.floor(
                    (brick.y - 55) / 31
                );

            color =
                colors[row % colors.length];

        }

        ctx.fillStyle = color;

        ctx.shadowBlur = 7;
        ctx.shadowColor = color;

        ctx.beginPath();

        ctx.roundRect(
            brick.x,
            brick.y,
            brick.w,
            brick.h,
            5
        );

        ctx.fill();

        ctx.shadowBlur = 0;

        if (brick.type === "bomb") {

            ctx.fillStyle = "white";
            ctx.font = "bold 15px Arial";
            ctx.textAlign = "center";

            ctx.fillText(
                "💣",
                brick.x + brick.w / 2,
                brick.y + 17
            );

        }

        if (brick.type === "strong") {

            ctx.fillStyle = "white";
            ctx.font = "bold 12px Arial";
            ctx.textAlign = "center";

            ctx.fillText(
                brick.hp,
                brick.x + brick.w / 2,
                brick.y + 16
            );

        }

    });

}

function drawPowerups() {

    powerups.forEach(p => {

        ctx.fillStyle = p.color;

        ctx.shadowBlur = 15;
        ctx.shadowColor = p.color;

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            13,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.shadowBlur = 0;

        ctx.fillStyle = "white";

        ctx.font = "bold 13px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            p.symbol,
            p.x,
            p.y + 5
        );

    });

}

function spawnPowerup(x, y) {

    let types = [

        {
            type: "expand",
            symbol: "↔",
            color: "#22c55e"
        },

        {
            type: "multi",
            symbol: "✦",
            color: "#facc15"
        },

        {
            type: "big",
            symbol: "●",
            color: "#06b6d4"
        },

        {
            type: "life",
            symbol: "♥",
            color: "#f43f5e"
        }

    ];

    if (Math.random() > .18)
        return;

    let p =
        types[
            Math.floor(
                Math.random() * types.length
            )
        ];

    powerups.push({

        x: x,
        y: y,

        dy: 2,

        type: p.type,
        symbol: p.symbol,
        color: p.color

    });

}

function collectPowerup(p) {

    if (p.type === "expand") {

        paddle.width =
            Math.min(
                paddle.width + 70,
                240
            );

        setTimeout(() => {

            paddle.width =
                paddle.normalWidth;

        }, 10000);

    }

    else if (p.type === "multi") {

        let original =
            balls[0];

        if (original) {

            balls.push(
                createBall(
                    original.x,
                    original.y,
                    -original.dx,
                    original.dy
                )
            );

            balls.push(
                createBall(
                    original.x,
                    original.y,
                    original.dx * .6,
                    original.dy
                )
            );

        }

    }

    else if (p.type === "big") {

        balls.forEach(b => {

            b.r = 16;

            setTimeout(() => {

                b.r = 9;

            }, 8000);

        });

    }

    else if (p.type === "life") {

        lives =
            Math.min(lives + 1, 5);

    }

    createParticles(
        p.x,
        p.y,
        p.color,
        20
    );

    updateUI();

}

function updatePowerups() {

    for (
        let i = powerups.length - 1;
        i >= 0;
        i--
    ) {

        let p = powerups[i];

        p.y += p.dy;

        if (
            p.y + 13 >= paddle.y &&
            p.y - 13 <=
                paddle.y + paddle.height &&
            p.x >= paddle.x &&
            p.x <=
                paddle.x + paddle.width
        ) {

            collectPowerup(p);

            powerups.splice(i, 1);

        }

        else if (p.y > H) {

            powerups.splice(i, 1);

        }

    }

}

function explodeBrick(brick) {

    createParticles(
        brick.x + brick.w / 2,
        brick.y + brick.h / 2,
        "#f97316",
        35
    );

    shake = 8;

    // 주변 벽돌까지 파괴
    bricks.forEach(other => {

        let dx =
            other.x - brick.x;

        let dy =
            other.y - brick.y;

        let distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (
            distance < 85 &&
            other.alive
        ) {

            other.alive = false;

            addScore(15);

            createParticles(
                other.x + other.w / 2,
                other.y + other.h / 2,
                "#ef4444",
                8
            );

        }

    });

}

function hitBrick(ball, brick) {

    if (!brick.alive)
        return;

    if (

        ball.x + ball.r > brick.x &&
        ball.x - ball.r <
            brick.x + brick.w &&
        ball.y + ball.r > brick.y &&
        ball.y - ball.r <
            brick.y + brick.h

    ) {

        ball.dy *= -1;

        brick.hp--;

        combo++;

        addScore(
            brick.type === "strong"
                ? 20
                : 10
        );

        createParticles(
            ball.x,
            ball.y,
            brick.type === "bomb"
                ? "#ef4444"
                : "#facc15",
            12
        );

        if (brick.type === "bomb") {

            brick.alive = false;

            explodeBrick(brick);

        }
        else if (brick.hp <= 0) {

            brick.alive = false;

            spawnPowerup(
                brick.x + brick.w / 2,
                brick.y + brick.h / 2
            );

        }

        // 콤보에 따른 속도 증가
        if (combo % 5 === 0) {

            balls.forEach(b => {

                b.dx *= 1.06;
                b.dy *= 1.06;

            });

        }

        return true;

    }

    return false;

}

function updateBalls() {

    for (
        let i = balls.length - 1;
        i >= 0;
        i--
    ) {

        let ball = balls[i];

        ball.trail.push({
            x: ball.x,
            y: ball.y
        });

        if (ball.trail.length > 8)
            ball.trail.shift();

        ball.x += ball.dx;
        ball.y += ball.dy;

        if (
            ball.x + ball.r >= W ||
            ball.x - ball.r <= 0
        ) {

            ball.dx *= -1;

        }

        if (
            ball.y - ball.r <= 0
        ) {

            ball.dy *= -1;

        }

        // 패들
        if (

            ball.y + ball.r >= paddle.y &&
            ball.y - ball.r <=
                paddle.y + paddle.height &&
            ball.x >= paddle.x &&
            ball.x <=
                paddle.x + paddle.width &&
            ball.dy > 0

        ) {

            let hit =
                (ball.x - paddle.x) /
                paddle.width;

            let angle =
                (hit - .5) *
                Math.PI *
                .8;

            let speed =
                Math.sqrt(
                    ball.dx * ball.dx +
                    ball.dy * ball.dy
                );

            ball.dx =
                Math.sin(angle) * speed;

            ball.dy =
                -Math.cos(angle) * speed;

            combo = Math.max(
                combo,
                0
            );

        }

        // 벽돌
        for (let brick of bricks) {

            if (hitBrick(ball, brick))
                break;

        }

        // 바닥
        if (
            ball.y - ball.r > H
        ) {

            balls.splice(i, 1);

        }

    }

    // 모든 공이 사라짐
    if (balls.length === 0) {

        lives--;

        combo = 0;

        updateUI();

        if (lives <= 0) {

            gameOver = true;
            running = false;

        }
        else {

            resetBalls();

        }

    }

}

function nextLevel() {

    let remaining =
        bricks.filter(
            b => b.alive
        ).length;

    if (remaining === 0) {

        level++;

        if (level > 8) {

            victory = true;
            gameOver = true;
            running = false;

            return;

        }

        createLevel();

        resetBalls();

        balls.forEach(b => {

            b.dx *=
                1 + level * .04;

            b.dy *=
                1 + level * .04;

        });

        createParticles(
            W / 2,
            H / 2,
            "#22c55e",
            60
        );

        updateUI();

    }

}

function update() {

    if (!running || paused || gameOver)
        return;

    updateBalls();

    updatePowerups();

    updateParticles();

    nextLevel();

    if (shake > 0)
        shake--;

}

function drawMessage() {

    if (running && !gameOver)
        return;

    ctx.fillStyle =
        "rgba(0,0,0,.65)";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    ctx.textAlign = "center";

    ctx.fillStyle = "white";

    ctx.font =
        "bold 44px Arial";

    if (victory) {

        ctx.fillText(
            "🏆 ALL CLEAR!",
            W / 2,
            H / 2 - 30
        );

    }
    else if (gameOver) {

        ctx.fillText(
            "GAME OVER",
            W / 2,
            H / 2 - 30
        );

    }
    else if (paused) {

        ctx.fillText(
            "⏸ PAUSED",
            W / 2,
            H / 2 - 30
        );

    }
    else {

        ctx.fillText(
            "🧱 BRICK BLAST",
            W / 2,
            H / 2 - 40
        );

    }

    ctx.font =
        "20px Arial";

    ctx.fillText(
        gameOver
            ? "다시 시작해서 도전하세요!"
            : "시작 버튼을 눌러 게임 시작",
        W / 2,
        H / 2 + 15
    );

}

function draw() {

    ctx.save();

    if (shake > 0) {

        ctx.translate(
            Math.random() * shake - shake / 2,
            Math.random() * shake - shake / 2
        );

    }

    drawBackground();

    drawBricks();

    drawPowerups();

    drawPaddle();

    drawBalls();

    drawParticles();

    ctx.restore();

    drawMessage();

}

function loop() {

    update();

    draw();

    requestAnimationFrame(loop);

}

function startGame() {

    if (gameOver) {

        restartGame();

    }

    running = true;
    paused = false;

}

function togglePause() {

    if (!running || gameOver)
        return;

    paused = !paused;

}

function restartGame() {

    score = 0;
    level = 1;
    lives = 3;
    combo = 0;

    running = false;
    paused = false;
    gameOver = false;
    victory = false;

    paddle.width =
        paddle.normalWidth;

    paddle.x =
        W / 2 -
        paddle.width / 2;

    powerups = [];
    particles = [];

    createLevel();
    resetBalls();

    updateUI();

}

// 마우스
canvas.addEventListener(
    "mousemove",
    e => {

        const rect =
            canvas.getBoundingClientRect();

        const x =
            (e.clientX - rect.left) *
            W /
            rect.width;

        paddle.x =
            x - paddle.width / 2;

        paddle.x =
            Math.max(
                0,
                Math.min(
                    W - paddle.width,
                    paddle.x
                )
            );

    }
);

// 모바일
canvas.addEventListener(
    "touchmove",
    e => {

        e.preventDefault();

        const rect =
            canvas.getBoundingClientRect();

        const x =
            (e.touches[0].clientX - rect.left) *
            W /
            rect.width;

        paddle.x =
            x - paddle.width / 2;

        paddle.x =
            Math.max(
                0,
                Math.min(
                    W - paddle.width,
                    paddle.x
                )
            );

    },
    { passive: false }
);

restartGame();

loop();

</script>

</body>
</html>
"""

components.html(
    html,
    height=680,
    scrolling=False
)
