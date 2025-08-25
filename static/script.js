function pollProgress(taskId) {
    const interval = setInterval(async () => {
        let resp = await axios.get(`/progress/${taskId}`);
        let progress = resp.data.progress;
        let bar = document.getElementById("progress-bar");
        bar.style.width = progress + "%";
        bar.innerText = progress + "%";

        if (progress >= 100 || progress === -1) {
            clearInterval(interval);
            let res = await axios.get(`/result/${taskId}`);
            let resultDiv = document.getElementById("result");
            if (progress === -1) {
                resultDiv.innerHTML = '<div class="alert alert-danger">Сталася помилка при конвертації!</div>';
            } else {
                let files = res.data.files;
                let html = '<h5>Готові файли:</h5><ul>';
                files.forEach(f => {
                    html += `<li><a href="/download/${f}" target="_blank">${f}</a></li>`;
                });
                html += '</ul>';
                resultDiv.innerHTML = html;
            }
        }
    }, 1000);
}

