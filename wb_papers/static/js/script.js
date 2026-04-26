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
const collegeSelect = document.getElementById('collegeSelect');
const streamSelect = document.getElementById('streamSelect');

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

// ── STREAM FILTER FOR AI LAB (matches by name, not ID) ──
document.addEventListener('DOMContentLoaded', function() {
    const aiCollegeSelect = document.querySelector('#dbSection #collegeSelect');
    const aiStreamSelect = document.querySelector('#dbSection #streamSelect');

    if (aiCollegeSelect && aiStreamSelect) {
        function filterAiStreams() {
            const selected = aiCollegeSelect.value;
            aiStreamSelect.querySelectorAll('option').forEach(opt => {
                if (!opt.value || opt.value === 'All') return;
                if (!selected || selected === 'All' || opt.dataset.college === selected) {
                    opt.style.display = '';
                } else {
                    opt.style.display = 'none';
                }
            });
            aiStreamSelect.value = 'All';
        }
        aiCollegeSelect.addEventListener('change', filterAiStreams);
        filterAiStreams();
    }
});

// ── SHOW MORE COLLEGES ON DASHBOARD ──
const showMoreBtn = document.getElementById('showMoreBtn');
if (showMoreBtn) {
    showMoreBtn.addEventListener('click', function() {
        document.querySelectorAll('.college-card-wrapper').forEach(card => {
            card.style.display = '';
        });
        this.style.display = 'none';
    });
}

// ── STREAM FILTER FOR MATERIALS PAGE ──
document.addEventListener('DOMContentLoaded', function() {
    const matCollegeSelect = document.getElementById('matCollegeSelect');
    const matStreamSelect = document.getElementById('matStreamSelect');

    if (matCollegeSelect && matStreamSelect) {
        function filterMatStreams() {
            const selected = matCollegeSelect.value;
            matStreamSelect.querySelectorAll('option').forEach(opt => {
                if (!opt.value) return;
                if (!selected || opt.dataset.college === selected) {
                    opt.style.display = '';
                } else {
                    opt.style.display = 'none';
                }
            });
            matStreamSelect.value = '';
        }
        matCollegeSelect.addEventListener('change', filterMatStreams);
        filterMatStreams();
    }
});

// ── UPLOAD MATERIAL: Hide college/stream/semester for Placement type ──
document.addEventListener('DOMContentLoaded', function() {
    const materialTypeSelect = document.getElementById('materialTypeSelect');
    const collegeStreamSection = document.getElementById('collegeStreamSection');

    if (materialTypeSelect && collegeStreamSection) {
        function toggleCollegeStream() {
            if (materialTypeSelect.value === 'PLACEMENT') {
                collegeStreamSection.style.display = 'none';
            } else {
                collegeStreamSection.style.display = '';
            }
        }
        materialTypeSelect.addEventListener('change', toggleCollegeStream);
        toggleCollegeStream(); // run on load
    }
});