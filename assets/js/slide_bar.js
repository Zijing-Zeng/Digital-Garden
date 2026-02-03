(function() {
    window.addEventListener('load', function() {
        var backToTopBtn = document.getElementById('backToTop');
        if (!backToTopBtn) return;

        // 检测是否为移动端 (屏幕小于 768px)
        var isMobile = window.innerWidth < 1024;

        var dock = document.createElement('div');
        dock.id = 'control-dock';

        // 如果不是移动端，才添加滑块
        if (!isMobile) {
            var sliderHTML =
                '<div class="slider-wrapper" title="调整页面宽度">' +
                    '<span style="font-size:14px; opacity:0.6; margin-right:8px;">↔</span>' +
                    '<input type="range" id="width-slider" min="1000" max="1600" step="10" value="1280">' +
                '</div>';
            dock.innerHTML = sliderHTML;
        }

        dock.appendChild(backToTopBtn);
        document.body.appendChild(dock);

        // 如果有滑块，绑定事件
        if (!isMobile) {
            var slider = document.getElementById('width-slider');
            var savedWidth = localStorage.getItem('pageWidth');

            if (savedWidth) {
                document.documentElement.style.setProperty('--page-max-width', savedWidth + 'px');
                slider.value = savedWidth;
            }

            slider.addEventListener('input', function(e) {
                var newWidth = e.target.value;
                document.documentElement.style.setProperty('--page-max-width', newWidth + 'px');
                localStorage.setItem('pageWidth', newWidth);
            });
        }
    });
})();