async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.start();

    mediaRecorder.addEventListener("dataavailable", async (event) => {
        const audioBlob = event.data;
        const formData = new FormData();
        formData.append("audio", audioBlob, "audio.wav");

        const response = await fetch("http://127.0.0.1:5000/speech-to-text", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        document.getElementById("output").innerText = result.text || result.error;
    });

    setTimeout(() => {
        mediaRecorder.stop();
    }, 5000); // 5 soniyadan keyin yozishni to'xtatadi
}
