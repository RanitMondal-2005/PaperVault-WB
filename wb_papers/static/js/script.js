
// -------------- Dash Board --------------------------

// ── SHOW MORE COLLEGES (Dashboard) ──
document.addEventListener('DOMContentLoaded', function() {
    const showMoreBtn = document.getElementById('showMoreBtn');
    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', function() {
            document.querySelectorAll('.college-card-wrapper').forEach(card => {
                card.style.display = ''; // Clears the inline style="display: none" and restores their default CSS layout so they immediately appear.
            });
            this.style.display = 'none'; // Hides the "Show All Institutes" button itself
        });
    }
});


// ---------------- Filter Logic ----------------------------


// ------------- College & Stream : Choice Hint in Filter page  ------------------
document.addEventListener('DOMContentLoaded', function () {
    const clg = document.querySelector('#collegeSelect');
    const strm = document.querySelector('#streamSelect');
    const hint = document.querySelector('#streamHint');

    if (!clg || !strm) return;

    function toggleStream() {
        if (clg.value === "") {
            strm.disabled = true;
            if (hint) hint.style.display = 'block';
        } else {
            strm.disabled = false;
            if (hint) hint.style.display = 'none';
        }
    }

    // Run on college change
    clg.addEventListener('change', toggleStream);

    // Run on page load
    toggleStream();
});


// ──--------------- JS STREAM FILTER ──---------------------

// Filters the stream dropdown based on the selected college.
// Each stream <option> must have a data-college="collegeId" attribute via HTML.
function applyStreamFilter(collegeSelect, streamSelect) {
    if (!collegeSelect || !streamSelect) return;

    // Show or hide each stream option based on whether it belongs to the selected college
    function filterStreams(resetSelection) {
        const selectedCollegeId = collegeSelect.value; // if the user selects the default option ("All Colleges"), the value is empty: "" and if the user selects an actual college, the value is the ID(pk) string (received via option value="{{ c.id }}"): e.g., "2"

        const streamOptionsList = Array.from(streamSelect.options); //Array.from() convert a list of HTML options into a true JavaScript array because in browsers, streamSelect.options looks like an array, but it is actually a HTMLOptionsCollection (an "array-like" object).

        streamOptionsList.forEach(function(option) {

            if (!option.value) return;

            // Check if the stream belongs to the selected college (or show all if no college is picked)
            const belongsToSelectedCollege = !selectedCollegeId || option.dataset.college === selectedCollegeId;// it contains True or False

            // Toggle option
            if (belongsToSelectedCollege) {
                option.style.display = ''; // overriding all inline style, so it restores the browser's default visibility for <option> elements, making the stream visible in the dropdown.
            } else {
                option.style.display = 'none';
            }
        });
        // Disable stream dropdown until a college is chosen
        if (selectedCollegeId === "") {
            streamSelect.disabled = true;  // Lock the Stream choice Box (Grey)
        } else {
            streamSelect.disabled = false; // Unlock it
        }

        // If college changed, clear the previously selected stream
        if (resetSelection) {
            streamSelect.value = '';
        }
    }

    // Run filter every time college selection dropdown changes
    collegeSelect.addEventListener('change', function() {
        filterStreams(true);
    });

    // Run once on every page load so pre-selected values from Django are respected
    setTimeout(function() {
        filterStreams(false);
    }, 50); // Small delay (50ms) ensures the DOM is fully ready before we read values
}

document.addEventListener('DOMContentLoaded', function() {

    //------------- Call the Stream Filter Function for each page -------------

    // ── 1. PAPERS SEARCH PAGE filter ──
    applyStreamFilter(
        document.getElementById('collegeSelect'),
        document.getElementById('streamSelect'),
    );

    // ── 2. PAPERS UPLOAD PAGE filter ──
    applyStreamFilter(
        document.getElementById('uploadCollegeSelect'),
        document.getElementById('uploadStreamSelect'),
    );

    // ── 3. MATERIALS SEARCH PAGE filter ──
    applyStreamFilter(
        document.getElementById('matCollegeSelect'),
        document.getElementById('matStreamSelect'),
    );

    // ──--------------- AI LAB filter ──------------------------
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
