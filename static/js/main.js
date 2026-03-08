/**
 * - Scroll: меняет стиль навбара при прокрутке
 * - Burger: открывает/закрывает мобильное меню
 * - Toggle password visibility: скрыть/показать пароль
 */

(function () {
    'use strict';

    const nav = document.getElementById('guestNav');
    const burger = document.getElementById('burger');
    const mobileMenu = document.getElementById('mobileMenu');

    //  Scroll: добавляет класс .scrolled на навбар
    function onScroll() {
        if (!nav) return;
        nav.classList.toggle('scrolled', window.scrollY > 40);
    }

    window.addEventListener('scroll', onScroll, {passive: true});
    onScroll(); // применить сразу при загрузке

    //  Burger: переключает мобильное меню
    function toggleMenu(force) {
        if (!burger || !mobileMenu) return;

        const isOpen = force !== undefined ? force : !burger.classList.contains('open');

        burger.classList.toggle('open', isOpen);
        mobileMenu.classList.toggle('open', isOpen);
        burger.setAttribute('aria-expanded', String(isOpen));
    }

    if (burger) {
        burger.addEventListener('click', function () {
            toggleMenu();
        });
    }

    // Закрыть меню при клике на ссылку внутри drawer
    if (mobileMenu) {
        mobileMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                toggleMenu(false);
            });
        });
    }

    // Закрыть меню при клике вне навбара
    document.addEventListener('click', function (e) {
        if (nav && !nav.contains(e.target)) {
            toggleMenu(false);
        }
    });

    // Закрыть меню при изменении размера окна (переход на десктоп)
    window.addEventListener('resize', function () {
        if (window.innerWidth > 700) {
            toggleMenu(false);
        }
    });
})();

// Toggle: password visibility
function togglePassword(inputId, iconEl) {
    var input = document.getElementById(inputId);
    if (!input) return;

    var isHidden = input.type === 'password';
    input.type = isHidden ? 'text' : 'password';

    // Swap icon: eye / eye-off
    iconEl.innerHTML = isHidden
        ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'
        : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
}

//  App nav: burger 
(function () {
    var appBurger = document.getElementById('appBurger');
    var appMobileMenu = document.getElementById('appMobileMenu');

    function toggleAppMenu(force) {
        if (!appBurger || !appMobileMenu) return;
        var isOpen = force !== undefined ? force : !appBurger.classList.contains('open');
        appBurger.classList.toggle('open', isOpen);
        appMobileMenu.classList.toggle('open', isOpen);
        appBurger.setAttribute('aria-expanded', String(isOpen));
    }

    if (appBurger) {
        appBurger.addEventListener('click', function (e) {
            e.stopPropagation();
            toggleAppMenu();
        });
    }

    if (appMobileMenu) {
        appMobileMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                toggleAppMenu(false);
            });
        });
    }

    window.addEventListener('resize', function () {
        if (window.innerWidth > 700) toggleAppMenu(false);
    });
})();

// Dropdown panels + mobile overlay + swipe-to-close
(function () {

    function isMobile() {
        return window.innerWidth <= 700;
    }

    // Закрыть все панели
    function closeAll() {
        document.querySelectorAll('.dd-panel.open').forEach(function (p) {
            p.classList.remove('open');
        });
        document.querySelectorAll('[aria-expanded="true"]').forEach(function (b) {
            b.setAttribute('aria-expanded', 'false');
        });
    }

    // Свайп вниз для закрытия панели
    function addSwipe(panel) {
        var startY = 0;
        var curY = 0;
        var dragging = false;

        panel.addEventListener('touchstart', function (e) {
            // Свайп только если скролл панели в самом верху
            if (panel.scrollTop > 0) return;
            startY = e.touches[0].clientY;
            curY = startY;
            dragging = true;
            panel.style.transition = 'none';
        }, {passive: true});

        panel.addEventListener('touchmove', function (e) {
            if (!dragging) return;
            curY = e.touches[0].clientY;
            var delta = curY - startY;
            if (delta > 0) {
                panel.style.transform = 'translateY(' + delta + 'px)';
            }
        }, {passive: true});

        panel.addEventListener('touchend', function () {
            if (!dragging) return;
            dragging = false;
            panel.style.transition = '';

            var delta = curY - startY;
            if (delta > 90) {
                // Достаточно далеко — закрыть
                panel.classList.add('swiping-out');
                setTimeout(function () {
                    panel.classList.remove('open', 'swiping-out');
                    panel.style.transform = '';
                    closeAll();
                }, 220);
            } else {
                // Вернуть на место
                panel.style.transform = '';
            }
        });
    }

    // Ручка (sheet handle)
    function ensureHandle(panel) {
        if (panel.querySelector('.sheet-handle')) return;
        var handle = document.createElement('div');
        handle.className = 'sheet-handle';
        panel.insertBefore(handle, panel.firstChild);
    }

    // Создание дропдауна
    function makeDropdown(btnId, panelId) {
        var btn = document.getElementById(btnId);
        var panel = document.getElementById(panelId);
        if (!btn || !panel) return;

        // Не даём клику по панели всплыть до document и не закрываем её
        panel.addEventListener('click', function (e) {
            e.stopPropagation();
        });

        addSwipe(panel);

        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            var isOpen = panel.classList.contains('open');

            // Сначала закрыть все
            closeAll();

            if (!isOpen) {
                if (isMobile()) ensureHandle(panel);
                panel.classList.add('open');
                btn.setAttribute('aria-expanded', 'true');
            }
        });
    }

    makeDropdown('btnNotif', 'notifPanel');
    makeDropdown('btnUser', 'userPanel');

    // Клик вне панели (десктоп) — закрыть
    document.addEventListener('click', closeAll);

})();