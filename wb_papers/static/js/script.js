// ---------- 1. DASHBOARD INTERACTIONS ---------------------------

// ──------- SHOW MORE COLLEGES Button ──-------──-------
document.addEventListener('DOMContentLoaded', function() {
    const showMoreBtn = document.getElementById('showMoreBtn');
    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', function() {
            document.querySelectorAll('.college-card-wrapper').forEach(card => {
                card.style.display = ''; // Clears the inline style="display: none" and restores their default CSS layout so they immediately appear.
            });
            this.style.display = 'none'; // Hides the "Show All Institutes" button itself after reveal
        });
    }
});


//----------- 2. JS STREAM FILTER (CORE)---------------------------


// ------------- Stream Choice Helper Text ------------------
function setupStreamHint(collegeSelect, hintElement) {
    if (!collegeSelect || !hintElement) return;

    function toggleHint() {
        if (collegeSelect.value === "") {
            hintElement.style.display = 'block';
        } else {
            hintElement.style.display = 'none';
        }
    }

    collegeSelect.addEventListener('change', toggleHint); // Check again whenever the college selection changes
    toggleHint(); // Run on initial load
}


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


//--------------------------- 3. APPLICATION INITIALIZATION ---------------------------

document.addEventListener('DOMContentLoaded', function() {

    // ── 1. Papers Search Page ──
    applyStreamFilter(
        document.getElementById('collegeSelect'),
        document.getElementById('streamSelect')
    );
    setupStreamHint(
        document.getElementById('collegeSelect'),
        document.getElementById('streamHint')
    );

    // ── 2. Papers Upload Page ──
    applyStreamFilter(
        document.getElementById('uploadCollegeSelect'),
        document.getElementById('uploadStreamSelect')
    );
    setupStreamHint(
        document.getElementById('uploadCollegeSelect'),
        document.getElementById('uploadStreamHint')
    );

    // ── 3. Materials Search Page ──
    applyStreamFilter(
        document.getElementById('matCollegeSelect'),
        document.getElementById('matStreamSelect')
    );
    setupStreamHint(
        document.getElementById('matCollegeSelect'),
        document.getElementById('matStreamHint')
    );

    // ── 4. AI Lab Form ──
    applyStreamFilter(
        document.getElementById('aiCollegeSelect'),
        document.getElementById('aiStreamSelect')
    );
    setupStreamHint(
        document.getElementById('aiCollegeSelect'),
        document.getElementById('aiStreamHint')
    );


    // ----------------------------------------------------------------

    // ── Upload Material: Toggle Semester for Placement Notes ──
    const materialTypeSelect = document.getElementById('materialTypeSelect');
    const uploadSemesterField = document.getElementById('uploadSemesterField');
    if (materialTypeSelect && uploadSemesterField) {
        function toggleSemester() {
            uploadSemesterField.style.display = materialTypeSelect.value === 'PLACEMENT' ? 'none' : '';
        }
        materialTypeSelect.addEventListener('change', toggleSemester);
        toggleSemester();
    }


    // ── Materials Page: Dynamic Field Toggling ──
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


    // ── Submit Button Spinner (For ai_sleect_subject & ai_lab_form buttons)──
    document.querySelectorAll('form').forEach(function(form) {

        form.addEventListener('submit', function() {
            const btn = form.querySelector('.js-loading-btn');
            if (!btn) return;

            const textSpan = btn.querySelector('.btn-text');
            const loadingSpan = btn.querySelector('.btn-loading');

            if (textSpan && loadingSpan) {
                textSpan.classList.add('d-none');
                loadingSpan.classList.remove('d-none');
            }

            setTimeout(function() { // Disable the button itself to avoid mutiple submit clicks
                btn.disabled = true;
            }, 0);
        });
    });
});

