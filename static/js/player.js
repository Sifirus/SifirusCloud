/**
 * SifirusCloud — Глобальный аудиоплеер
 *
 * API:
 *   Player.loadQueue(tracks, startIndex)  — загрузить очередь
 *   Player.play()                          — запустить воспроизведение
 *   Player.pause()                         — пауза
 *   Player.next()                          — следующий трек
 *   Player.prev()                          — предыдущий трек
 *
 * Каждый элемент tracks = { id, url, title, artist, cover }
 */

(function () {
    'use strict';

    // ── Элементы DOM ──
    const playerEl   = document.getElementById('mainPlayer');
    const audio      = document.getElementById('main-audio');
    if (!playerEl || !audio) return;

    const btnPlay    = document.getElementById('btn-play');
    const playIcon   = document.getElementById('play-icon');
    const btnPrev    = document.getElementById('btn-prev');
    const btnNext    = document.getElementById('btn-next');
    const btnShuffle = document.getElementById('btn-shuffle');
    const btnRepeat  = document.getElementById('btn-repeat');
    const btnVol     = document.getElementById('btn-vol');
    const btnHeart   = document.getElementById('p-heart');

    const pTitle     = document.getElementById('p-title');
    const pAuthor    = document.getElementById('p-author');
    const pThumb     = document.getElementById('p-thumb');
    const pThumbImg  = document.getElementById('p-thumb-img');
    const pThumbSvg  = document.getElementById('p-thumb-svg');

    const timeCur    = document.getElementById('p-time-cur');
    const timeTotal  = document.getElementById('p-time-total');
    const progBar    = document.getElementById('p-prog-bar');
    const progFill   = document.getElementById('p-prog-fill');
    const volBar     = document.getElementById('p-vol-bar');
    const volFill    = document.getElementById('p-vol-fill');

    // ── Состояние ──
    let queue       = [];
    let currentIdx  = 0;
    let isPlaying   = false;
    let isShuffle   = false;
    let repeatMode  = 0;  // 0=off, 1=all, 2=one
    let volume      = 0.65;

    audio.volume = volume;

    // ── Иконки play/pause (SVG paths) ──
    const PLAY_POINTS  = '13 10 25 17 13 24';
    const PAUSE_POINTS = null; // используем два rect для паузы

    function setPlayIcon() {
        btnPlay.innerHTML = `<svg width="34" height="34" viewBox="0 0 34 34">
            <circle cx="17" cy="17" r="17" fill="#3b82f6"/>
            <polygon points="14 10 26 17 14 24" fill="white"/>
        </svg>`;
    }

    function setPauseIcon() {
        btnPlay.innerHTML = `<svg width="34" height="34" viewBox="0 0 34 34">
            <circle cx="17" cy="17" r="17" fill="#3b82f6"/>
            <rect x="12" y="10" width="4" height="14" rx="1" fill="white"/>
            <rect x="19" y="10" width="4" height="14" rx="1" fill="white"/>
        </svg>`;
    }

    // ── Форматирование времени ──
    function fmt(sec) {
        if (!sec || isNaN(sec)) return '0:00';
        const m = Math.floor(sec / 60);
        const s = Math.floor(sec % 60).toString().padStart(2, '0');
        return m + ':' + s;
    }

    // ── Загрузка трека ──
    function loadTrack(idx) {
        if (idx < 0 || idx >= queue.length) return;
        currentIdx = idx;
        const t = queue[idx];

        audio.src = t.url;
        audio.load();

        pTitle.textContent  = t.title || '—';
        pAuthor.textContent = t.artist || '—';

        if (t.cover) {
            pThumbImg.src = t.cover;
            pThumbImg.style.display = 'block';
            if (pThumbSvg) pThumbSvg.style.display = 'none';
        } else {
            pThumbImg.style.display = 'none';
            if (pThumbSvg) pThumbSvg.style.display = '';
        }

        progFill.style.width = '0%';
        timeCur.textContent  = '0:00';
        timeTotal.textContent = '0:00';

        playerEl.style.display = '';

        // Подсветка строки в плейлисте
        document.querySelectorAll('.pl-track-row').forEach(r => r.classList.remove('playing'));
        const row = document.querySelector(`.pl-track-row[data-track-id="${t.id}"]`);
        if (row) row.classList.add('playing');
    }

    // ── Play / Pause ──
    let lastPlayedId = null;

    function play() {
        if (!queue.length) return;
        audio.play().then(() => {
            isPlaying = true;
            setPauseIcon();

            // Засчитать прослушивание (один раз за загрузку трека)
            const t = queue[currentIdx];
            if (t && t.id && t.id !== lastPlayedId) {
                lastPlayedId = t.id;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
                    || document.cookie.split(';').map(c => c.trim()).find(c => c.startsWith('csrftoken='))?.split('=')[1]
                    || '';
                fetch('/track/' + t.id + '/play/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                }).catch(() => {});
            }
        }).catch(() => {});
    }

    function pause() {
        audio.pause();
        isPlaying = false;
        setPlayIcon();
    }

    function togglePlay() {
        if (isPlaying) pause();
        else play();
    }

    // ── Next / Prev ──
    function next() {
        if (!queue.length) return;
        if (repeatMode === 2) {
            // Repeat one: перезапуск
            audio.currentTime = 0;
            play();
            return;
        }
        let nextIdx = currentIdx + 1;
        if (nextIdx >= queue.length) {
            if (repeatMode === 1) nextIdx = 0;  // Repeat all
            else { pause(); return; }
        }
        loadTrack(nextIdx);
        play();
    }

    function prev() {
        if (!queue.length) return;
        // Если больше 3 сек — перемотать в начало
        if (audio.currentTime > 3) {
            audio.currentTime = 0;
            return;
        }
        let prevIdx = currentIdx - 1;
        if (prevIdx < 0) prevIdx = repeatMode === 1 ? queue.length - 1 : 0;
        loadTrack(prevIdx);
        play();
    }

    // ── Shuffle ──
    function toggleShuffle() {
        isShuffle = !isShuffle;
        btnShuffle.style.color = isShuffle ? '#3b82f6' : '';
        if (isShuffle && queue.length > 1) {
            const current = queue[currentIdx];
            const rest = queue.filter((_, i) => i !== currentIdx);
            rest.sort(() => Math.random() - 0.5);
            queue = [current, ...rest];
            currentIdx = 0;
        }
    }

    // ── Repeat ──
    function toggleRepeat() {
        repeatMode = (repeatMode + 1) % 3;
        if (repeatMode === 0) {
            btnRepeat.style.color = '';
            btnRepeat.title = 'Зациклить';
        } else if (repeatMode === 1) {
            btnRepeat.style.color = '#3b82f6';
            btnRepeat.title = 'Повтор всех';
        } else {
            btnRepeat.style.color = '#8b5cf6';
            btnRepeat.title = 'Повтор одного';
        }
    }

    // ── Прогресс ──
    audio.addEventListener('timeupdate', () => {
        if (!audio.duration) return;
        const pct = (audio.currentTime / audio.duration) * 100;
        progFill.style.width = pct + '%';
        timeCur.textContent = fmt(audio.currentTime);
    });

    audio.addEventListener('loadedmetadata', () => {
        timeTotal.textContent = fmt(audio.duration);
    });

    audio.addEventListener('ended', () => {
        next();
    });

    // Клик по прогресс-бару — перемотка
    progBar.addEventListener('click', (e) => {
        if (!audio.duration) return;
        const rect = progBar.getBoundingClientRect();
        const pct = (e.clientX - rect.left) / rect.width;
        audio.currentTime = pct * audio.duration;
    });

    // Громкость
    volBar.addEventListener('click', (e) => {
        const rect = volBar.getBoundingClientRect();
        volume = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        audio.volume = volume;
        volFill.style.width = (volume * 100) + '%';
    });

    btnVol.addEventListener('click', () => {
        if (audio.volume > 0) {
            audio.volume = 0;
            volFill.style.width = '0%';
        } else {
            audio.volume = volume || 0.65;
            volFill.style.width = (audio.volume * 100) + '%';
        }
    });

    // Лайк (визуально)
    if (btnHeart) {
        btnHeart.addEventListener('click', () => {
            const isLiked = btnHeart.style.color === 'rgb(239, 68, 68)';
            btnHeart.style.color = isLiked ? '#94a3b8' : '#ef4444';
            btnHeart.querySelector('svg').style.fill = isLiked ? 'none' : '#ef4444';
        });
    }

    // ── Подключение кнопок ──
    btnPlay.addEventListener('click', togglePlay);
    btnNext.addEventListener('click', next);
    btnPrev.addEventListener('click', prev);
    btnShuffle.addEventListener('click', toggleShuffle);
    btnRepeat.addEventListener('click', toggleRepeat);

    // ── Горячие клавиши ──
    document.addEventListener('keydown', (e) => {
        // Не перехватываем, если фокус в input/textarea
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;

        if (e.code === 'Space') {
            e.preventDefault();
            togglePlay();
        } else if (e.code === 'ArrowRight' && e.shiftKey) {
            next();
        } else if (e.code === 'ArrowLeft' && e.shiftKey) {
            prev();
        } else if (e.code === 'ArrowRight') {
            audio.currentTime = Math.min(audio.duration, audio.currentTime + 5);
        } else if (e.code === 'ArrowLeft') {
            audio.currentTime = Math.max(0, audio.currentTime - 5);
        }
    });

    // ── Публичный API ──
    window.Player = {
        loadQueue: function (tracks, startIndex) {
            queue = [...tracks];
            loadTrack(startIndex || 0);
        },
        play: play,
        pause: pause,
        next: next,
        prev: prev,
        isPlaying: function () { return isPlaying; },
        getQueue: function () { return queue; },

        // Быстрый запуск одного трека (для страниц без плейлиста)
        playSingle: function (trackData) {
            queue = [trackData];
            loadTrack(0);
            play();
        }
    };

})();
