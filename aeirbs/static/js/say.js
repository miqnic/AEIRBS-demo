function say(m) {
    var synth = window.speechSynthesis;

    var msg = new SpeechSynthesisUtterance();
    var voices = window.speechSynthesis.getVoices();
    msg.voice = voices[6];
    msg.volume = 3;
    msg.rate = 1;
    msg.pitch = 1;
    msg.text = m;
    msg.lang = 'en-UK';
    
    return [synth, msg];
}