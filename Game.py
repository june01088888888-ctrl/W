import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌 깨기",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌 깨기")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {
        margin: 0;
        background: #111827;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
        overflow: hidden;
    }

    #game {
        display: block;
        margin: 10px auto;
        background: #0f172a;
        border: 3px solid #475569;
        border-radius: 12px;
        max-width: 100%;
        cursor: none;
    }

    #info {
        font-size: 18px;
        margin: 8px;
    }

    button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 10px 22px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }

    button:hover {
        background: #1d4ed8;
    }
</style>
</head>

<body>

<div id="info">
    점수: <span id="score">0</span>
    &nbsp;&nbsp; 목숨: <span id="lives">3</span>
</div>

<canvas id="game" width="720" height="520"></canvas>

<button onclick="restartGame()">🔄 다시 시작</button>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

let score = 0;
let lives = 3;
let gameOver = false;
let won = false;

const paddle = {
    width: 120,
    height: 14,
    x: W / 2 - 60,
    y: H - 35,
    speed: 9
};

const ball = {
    x: W / 2,
    y: H - 60,
    radius: 9,
    dx: 4,
    dy: -4
};

const brickRows = 6;
const brickCols = 10;
const brickWidth = 62;
const brickHeight = 22;
const brickGap = 8;

const totalBrickWidth =
    brickCols * brickWidth +
    (brickCols - 1) * brickGap;

const brickStartX = (W - totalBrickWidth) / 2;
const brickStartY = 55;

let bricks = [];

function createBricks() {
    bricks = [];

    for (let r = 0; r < brickRows; r++) {
        for (let c = 0; c < brickCols; c++) {
            bricks.push({
                x: brickStartX + c * (brickWidth + brickGap),
                y: brickStartY + r * (brickHeight + brickGap),
                width: brickWidth,
                height: brickHeight,
                alive: true
            });
        }
    }
}

createBricks();

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#facc15";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.fillStyle = "#38bdf8";
    ctx.beginPath();
    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        7
    );
    ctx.fill();
}

function drawBricks() {
    bricks.forEach((brick, i) => {
        if (!brick.alive) return;

        const colors = [
            "#ef4444",
            "#f97316",
            "#eab308",
            "#22c55e",
            "#06b6d4",
            "#8b5cf6"
        ];

        ctx.fillStyle = colors[Math.floor(i / brickCols)];

        ctx.beginPath();
        ctx.roundRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height,
            4
        );
        ctx.fill();
    });
}

function drawBackground() {
    ctx.fillStyle = "#0f172a";
    ctx.fillRect(0, 0, W, H);
}

function updateScore() {
    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;
}

function collisionDetection() {
    for (const brick of bricks) {
        if (!brick.alive) continue;

        if (
            ball.x + ball.radius > brick.x &&
            ball.x - ball.radius < brick.x + brick.width &&
            ball.y + ball.radius > brick.y &&
            ball.y - ball.radius < brick.y + brick.height
        ) {
            brick.alive = false;
            ball.dy *= -1;
            score += 10;

            if (score >= brickRows * brickCols * 10) {
                won = true;
                gameOver = true;
            }

            updateScore();
            break;
        }
    }
}

function resetBall() {
    ball.x = W / 2;
    ball.y = H - 60;

    ball.dx = (Math.random() > 0.5 ? 1 : -1) * 4;
    ball.dy = -4;
}

function update() {
    if (gameOver) return;

    ball.x += ball.dx;
    ball.y += ball.dy;

    // 좌우 벽
    if (
        ball.x + ball.radius >= W ||
        ball.x - ball.radius <= 0
    ) {
        ball.dx *= -1;
    }

    // 위쪽 벽
    if (ball.y - ball.radius <= 0) {
        ball.dy *= -1;
    }

    // 패들 충돌
    if (
        ball.y + ball.radius >= paddle.y &&
        ball.y - ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width &&
        ball.dy > 0
    ) {
        const hitPosition =
            (ball.x - paddle.x) / paddle.width;

        const angle =
            (hitPosition - 0.5) * Math.PI * 0.8;

        const speed =
            Math.sqrt(ball.dx ** 2 + ball.dy ** 2);

        ball.dx = Math.sin(angle) * speed;
        ball.dy = -Math.cos(angle) * speed;
    }

    // 바닥
    if (ball.y - ball.radius > H) {
        lives--;
        updateScore();

        if (lives <= 0) {
            gameOver = true;
        } else {
            resetBall();
        }
    }

    collisionDetection();
}

function drawMessage() {
    if (!gameOver) return;

    ctx.fillStyle = "rgba(0,0,0,0.65)";
    ctx.fillRect(0, 0, W, H);

    ctx.textAlign = "center";

    ctx.fillStyle = "white";
    ctx.font = "bold 42px Arial";

    if (won) {
        ctx.fillText("🎉 YOU WIN!", W / 2, H / 2 - 20);
    } else {
        ctx.fillText("GAME OVER", W / 2, H / 2 - 20);
    }

    ctx.font = "20px Arial";
    ctx.fillText(
        "다시 시작 버튼을 눌러주세요",
        W / 2,
        H / 2 + 25
    );
}

function draw() {
    drawBackground();
    drawBricks();
    drawPaddle();
    drawBall();
    drawMessage();
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

canvas.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();

    const mouseX =
        (e.clientX - rect.left) *
        (canvas.width / rect.width);

    paddle.x = mouseX - paddle.width / 2;

    if (paddle.x < 0)
        paddle.x = 0;

    if (paddle.x + paddle.width > W)
        paddle.x = W - paddle.width;
});

// 모바일 터치
canvas.addEventListener("touchmove", (e) => {
    e.preventDefault();

    const rect = canvas.getBoundingClientRect();

    const touchX =
        (e.touches[0].clientX - rect.left) *
        (canvas.width / rect.width);

    paddle.x = touchX - paddle.width / 2;

    if (paddle.x < 0)
        paddle.x = 0;

    if (paddle.x + paddle.width > W)
        paddle.x = W - paddle.width;
}, { passive: false });

function restartGame() {
    score = 0;
    lives = 3;
    gameOver = false;
    won = false;

    paddle.x = W / 2 - paddle.width / 2;

    createBricks();
    resetBall();
    updateScore();
}

updateScore();
gameLoop();
</script>

</body>
</html>
"""

components.html(game_html, height=600, scrolling=False)
