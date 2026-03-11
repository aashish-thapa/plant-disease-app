document.addEventListener("DOMContentLoaded", function () {
    initNavToggle();
    initUploadZone();
    initFlashDismiss();
    initAnalyzeLoader();
});


function initNavToggle() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".navbar-nav");
    if (!toggle || !nav) return;

    toggle.addEventListener("click", function () {
        nav.classList.toggle("open");
    });
}


function initUploadZone() {
    var zone = document.getElementById("upload-zone");
    var input = document.getElementById("image-input");
    var preview = document.getElementById("upload-preview");
    var previewImg = document.getElementById("preview-img");
    var previewName = document.getElementById("preview-name");
    var cameraBtn = document.getElementById("camera-btn");
    var cameraInput = document.getElementById("camera-input");

    if (!zone || !input) return;

    zone.addEventListener("click", function () {
        input.click();
    });

    zone.addEventListener("dragover", function (e) {
        e.preventDefault();
        zone.classList.add("dragover");
    });

    zone.addEventListener("dragleave", function () {
        zone.classList.remove("dragover");
    });

    zone.addEventListener("drop", function (e) {
        e.preventDefault();
        zone.classList.remove("dragover");
        if (e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            showPreview(e.dataTransfer.files[0]);
        }
    });

    input.addEventListener("change", function () {
        if (input.files.length) {
            showPreview(input.files[0]);
        }
    });

    if (cameraBtn && cameraInput) {
        cameraBtn.addEventListener("click", function () {
            cameraInput.click();
        });
        cameraInput.addEventListener("change", function () {
            if (cameraInput.files.length) {
                var dt = new DataTransfer();
                dt.items.add(cameraInput.files[0]);
                input.files = dt.files;
                showPreview(cameraInput.files[0]);
            }
        });
    }

    function showPreview(file) {
        var allowed = ["image/jpeg", "image/png"];
        if (allowed.indexOf(file.type) === -1) {
            alert("Only JPEG and PNG images are accepted.");
            input.value = "";
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            alert("File must be under 10 MB.");
            input.value = "";
            return;
        }

        var reader = new FileReader();
        reader.onload = function (e) {
            if (previewImg) previewImg.src = e.target.result;
            if (previewName) previewName.textContent = file.name;
            if (preview) preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
}


function initAnalyzeLoader() {
    var form = document.getElementById("upload-form");
    if (!form) return;

    form.addEventListener("submit", function () {
        var btn = form.querySelector(".btn-analyze");
        if (!btn) return;

        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Analyzing...';

        // Show the overlay
        var overlay = document.getElementById("loading-overlay");
        if (overlay) overlay.classList.add("visible");
    });
}


function initFlashDismiss() {
    var alerts = document.querySelectorAll(".alert[data-dismiss]");
    alerts.forEach(function (el) {
        setTimeout(function () {
            el.style.opacity = "0";
            el.style.transition = "opacity 0.4s";
            setTimeout(function () { el.remove(); }, 400);
        }, 4000);
    });
}
