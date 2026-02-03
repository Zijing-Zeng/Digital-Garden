/* static/js/constellation.js - v2.0 修复鼠标连线 */
(function() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // 样式设置
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';

    // Z-index 稍微低一点，确保它在内容之下，但在背景之上
    // 如果想要点击特效生效，pointerEvents 不能完全 none，
    // 但为了不阻挡网页点击，通常设为 none，点击事件绑定在 window 上即可
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';

    document.body.appendChild(canvas);

    let width, height;
    let particles = [];
    let stars = [];
    // 初始化鼠标位置在屏幕外，避免刚打开页面时左上角汇聚
    const mouse = { x: -9999, y: -9999 };

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }
    window.addEventListener('resize', resize);
    resize();

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    window.addEventListener('click', (e) => {
        createExplosion(e.clientX, e.clientY);
    });

    // === 背景粒子 ===
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.size = Math.random() * 2 + 1;
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;
        }
        draw() {
            ctx.fillStyle = 'rgba(150, 150, 150, 0.5)';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    // === ✨ BlingBling 星星 (点击特效) ===
    class Star {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.vx = (Math.random() - 0.5) * 8;
            this.vy = (Math.random() - 0.5) * 8;
            this.alpha = 1;
            this.rotation = Math.random() * 360;
            this.scale = Math.random() * 0.6 + 0.8;
            const colors = ['255, 215, 0', '135, 206, 250', '255, 105, 180', '224, 255, 255'];
            this.baseColor = colors[Math.floor(Math.random() * colors.length)];
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.vx *= 0.94;
            this.vy *= 0.94;
            this.rotation += 2;
            this.alpha *= 0.96;
        }

        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation * Math.PI / 180);
            ctx.scale(this.scale, this.scale);
            ctx.beginPath();
            for (let i = 0; i < 5; i++) {
                ctx.lineTo(Math.cos((18 + i * 72) * Math.PI / 180) * 12,
                           -Math.sin((18 + i * 72) * Math.PI / 180) * 12);
                ctx.lineTo(Math.cos((54 + i * 72) * Math.PI / 180) * 5,
                           -Math.sin((54 + i * 72) * Math.PI / 180) * 5);
            }
            ctx.closePath();
            let gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, 12);
            gradient.addColorStop(0, `rgba(255, 255, 255, ${this.alpha})`);
            gradient.addColorStop(0.4, `rgba(${this.baseColor}, ${this.alpha})`);
            gradient.addColorStop(1, `rgba(${this.baseColor}, 0)`);
            ctx.fillStyle = gradient;
            ctx.fill();
            ctx.restore();
        }
    }

    // 初始化粒子
    for (let i = 0; i < 60; i++) { // 稍微增加一点粒子数，效果更好
        particles.push(new Particle());
    }

    function createExplosion(x, y) {
        for (let i = 0; i < 10; i++) {
            stars.push(new Star(x, y));
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        particles.forEach((p, index) => {
            p.update();
            p.draw();

            // 1. 粒子与粒子之间的连线
            for (let j = index + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 100) {
                    ctx.strokeStyle = `rgba(150, 150, 150, ${1 - dist/100})`; // 距离越远越淡
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            }

            // 2. [新增] 粒子与鼠标之间的连线
            const distMouse = Math.hypot(p.x - mouse.x, p.y - mouse.y);
            // 鼠标连线距离可以设大一点 (例如 150)，更有吸附感
            if (distMouse < 150) {
                // 颜色稍微深一点，突出交互感
                ctx.strokeStyle = `rgba(100, 149, 237, ${1 - distMouse/150})`;
                ctx.lineWidth = 0.8;
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.stroke();
            }
        });

        // 绘制点击爆炸的星星
        for (let i = 0; i < stars.length; i++) {
            stars[i].update();
            stars[i].draw();
            if (stars[i].alpha <= 0.05) {
                stars.splice(i, 1);
                i--;
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
})();