// static/script.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("pdfFile");
    const downloadSection = document.getElementById("downloadSection");
    const downloadLink = document.getElementById("downloadLink");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            alert("PDF 파일을 선택해주세요.");
            return;
        }

        const formData = new FormData();
        formData.append("pdf", file);

        try {
            const response = await fetch("/convert", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("서버 오류: 변환에 실패했습니다.");
            }

            const result = await response.json();

            if (result.success) {
                downloadLink.href = result.download_url;
                downloadSection.classList.remove("hidden");
            } else {
                alert("변환에 실패했습니다. 다시 시도해주세요.");
            }
        }
