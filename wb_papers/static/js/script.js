// This JS is only doing one thing — fetching the paper count for the stats bar number ( eg : the "50+" counter on the dashboard).

// ── STATS COUNTER ANIMATION ──
function animateCount(el, target, duration) {
    let start = 0;
    const step = Math.ceil(target / (duration / 30));
    const timer = setInterval(() => {
        start += step;
        if (start >= target) { start = target; clearInterval(timer); }
        el.textContent = start + '+';
    }, 30);
}
// ----------------------------------------------------------------------------------
// Fetch paper count and animate the stat on dashboard
const statEl = document.getElementById('stat-papers');
if (statEl) {
    fetch("/search/")
        .then(r => r.text())
        .then(html => {
            const match = html.match(/Page \d+ of (\d+)/);
            if (match) {
                animateCount(statEl, parseInt(match[1]) * 10, 1000);
            } else {
                statEl.textContent = '50+';
            }
        })
        .catch(() => { statEl.textContent = '50+'; });
}

// ── STREAM FILTER BY COLLEGE ──
const collegeSelect = document.getElementById('id_college') || document.querySelector('select[name="college"]');
const streamSelect = document.getElementById('stream-select');

function filterStreams() {
    if (!collegeSelect || !streamSelect) return;
    const selectedCollege = collegeSelect.value;
    const options = streamSelect.querySelectorAll('option');

    options.forEach(opt => {
        if (!opt.value) return; // keep "Select Stream" option
        if (!selectedCollege || opt.dataset.college === selectedCollege) {
            opt.style.display = '';
        } else {
            opt.style.display = 'none';
        }
    });

    // Reset stream if current selection doesn't match college
    const selected = streamSelect.querySelector('option:checked');
    if (selected && selected.dataset.college && selected.dataset.college !== selectedCollege) {
        streamSelect.value = '';
    }
}

if (collegeSelect) {
    collegeSelect.addEventListener('change', filterStreams);
    filterStreams(); // run on page load to respect pre-selected filters
}