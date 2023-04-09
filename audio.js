// Create a function to play the audio
function playAudio() {
    var audio = new Audio('a1.mp3');
    audio.play();
}

// Schedule the audio player at the specific times
var audio_times = [(2, 45), (12, 0), (15, 45), (18, 15), (20, 30)]
for (var i = 0; i < audio_times.length; i++) {
    var audioTime = new Date();
    audioTime.setHours(audio_times[i][0]);
    audioTime.setMinutes(audio_times[i][1]);

    var timeDiff = audioTime.getTime(); // play 5 minutes before the specific time

    if (timeDiff > 0) {
        setTimeout(playAudio, timeDiff);
        console.log(timeDiff);
    }
}
