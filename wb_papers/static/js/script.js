// -----------------------------
// PAPERVAULT WB — MAIN JS SCRIPT
// -----------------------------

// ── STATS COUNTER ANIMATION (Dashboard) ──
function animateCount(el, target, duration) {
    let start = 0;
    const step = Math.ceil(target / (duration / 30));
    const timer = setInterval(() => {
        start += step;
        if (start >= target) { start = target; clearInterval(timer); }
        el.textContent = start + '+';
    }, 30);
}

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

// ── SHOW MORE COLLEGES (Dashboard) ──
document.addEventListener('DOMContentLoaded', function() {
    const showMoreBtn = document.getElementById('showMoreBtn');
    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', function() {
            document.querySelectorAll('.college-card-wrapper').forEach(card => {
                card.style.display = '';
            });
            this.style.display = 'none';
        });
    }
});

// ── REUSABLE STREAM FILTER FUNCTION ──
// Works for any college+stream select pair using data-college attributes
function applyStreamFilter(collegeEl, streamEl, resetOnChange) {
    if (!collegeEl || !streamEl) return;

    function doFilter(reset) {
        const selected = collegeEl.value;
        let hasVisible = false;

        Array.from(streamEl.options).forEach(opt => {
            if (!opt.value) return;
            const belongs = !selected || opt.dataset.college === selected;
            opt.style.display = belongs ? '' : 'none';
            if (belongs) hasVisible = true;
        });

        // Lock stream dropdown if no college selected
        streamEl.disabled = !selected;

        if (reset) {
            const current = streamEl.querySelector('option:checked');
            if (current && current.dataset.college && current.dataset.college !== selected) {
                streamEl.value = '';
            }
        }
    }

    collegeEl.addEventListener('change', () => doFilter(true));
    // Small delay ensures Django's pre-selected values are read correctly
    setTimeout(() => doFilter(false), 50);
}

document.addEventListener('DOMContentLoaded', function() {

// ── PAPERS SEARCH PAGE filter ──
applyStreamFilter(
    document.getElementById('collegeSelect'),
    document.getElementById('streamSelect'),
    true
);

// ── PAPERS UPLOAD PAGE filter ──
applyStreamFilter(
    document.getElementById('uploadCollegeSelect'),
    document.getElementById('uploadStreamSelect'),
    true
);

// ── MATERIALS SEARCH PAGE filter ──
applyStreamFilter(
    document.getElementById('matCollegeSelect'),
    document.getElementById('matStreamSelect'),
    true
);

// ── AI LAB filter ──
const aiCollegeSelect = document.querySelector('#dbSection select[name="institution"]');
const aiStreamSelect = document.querySelector('#dbSection select[name="stream"]');
if (aiCollegeSelect && aiStreamSelect) {
    function filterAiStreams() {
        const selected = aiCollegeSelect.value;
        Array.from(aiStreamSelect.options).forEach(opt => {
            if (!opt.value || opt.value === 'All') return;
            opt.style.display = (!selected || selected === 'All' || opt.dataset.college === selected) ? '' : 'none';
        });
        // Lock stream if no college selected
        aiStreamSelect.disabled = (!selected || selected === 'All');
        aiStreamSelect.value = 'All';
    }
    aiCollegeSelect.addEventListener('change', filterAiStreams);
    // Run on page load
    setTimeout(() => filterAiStreams(), 50);
}

// ── UPLOAD MATERIAL: Hide semester for Placement Notes ──
const materialTypeSelect = document.getElementById('materialTypeSelect');
const uploadSemesterField = document.getElementById('uploadSemesterField');
if (materialTypeSelect && uploadSemesterField) {
    function toggleSemester() {
        uploadSemesterField.style.display = materialTypeSelect.value === 'PLACEMENT' ? 'none' : '';
    }
    materialTypeSelect.addEventListener('change', toggleSemester);
    toggleSemester();
}

// ── MATERIALS PAGE: Toggle fields by type ──
const matTypeSelect = document.getElementById('matTypeSelect');
const streamField = document.getElementById('streamField');
const semesterField = document.getElementById('semesterField');
const subjectField = document.getElementById('subjectField');
const placementSubjectSelect = document.getElementById('placementSubjectSelect');

if (matTypeSelect) {
    function toggleMaterialFields() {
        const isPlacement = matTypeSelect.value === 'PLACEMENT';
        if (streamField) streamField.classList.toggle('d-none', isPlacement);
        if (semesterField) semesterField.classList.toggle('d-none', isPlacement);
        if (subjectField) subjectField.classList.toggle('d-none', !isPlacement);
        if (isPlacement && placementSubjectSelect && placementSubjectSelect.options.length <= 1) {
            loadPlacementSubjects();
        }
    }

    function loadPlacementSubjects() {
        fetch('/materials/api/placement-subjects/')
            .then(r => r.json())
            .then(data => {
                placementSubjectSelect.innerHTML = '<option value="">All Subjects</option>';
                data.subjects.forEach(sub => {
                    const opt = document.createElement('option');
                    opt.value = sub;
                    opt.textContent = sub;
                    placementSubjectSelect.appendChild(opt);
                });
            })
            .catch(() => {});
    }

    matTypeSelect.addEventListener('change', toggleMaterialFields);
    toggleMaterialFields();
}

// ── AI LAB FORM: Continue to Analysis button ──
const continueForm = document.querySelector('form[action*="ai-lab/select-subject"]');
if (continueForm) {
    continueForm.addEventListener('submit', function() {
        const btn = document.getElementById('continueBtn');
        if (btn) {
            document.getElementById('continueBtnText')?.classList.add('d-none');
            document.getElementById('continueBtnLoading')?.classList.remove('d-none');
            btn.disabled = true;
        }
    });
}

// ── AI SELECT SUBJECT: Analyze Now button ──
const analyzeForm = document.querySelector('form[action*="ai-lab/analyze"]');
if (analyzeForm) {
    analyzeForm.addEventListener('submit', function() {
        const btn = document.getElementById('analyzeBtn');
        if (btn) {
            document.getElementById('btnText')?.classList.add('d-none');
            document.getElementById('btnLoading')?.classList.remove('d-none');
            btn.disabled = true;
        }
    });
}
});