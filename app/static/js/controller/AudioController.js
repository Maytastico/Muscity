class AudioController{
    static getAllTitles(){
        let loading = new Dialog({
            generateOverlay: true,
            open: true,
            type: "loading",
            feedbackMsg: "Getting Data..."
        });
        fetch('http://localhost:5000/api/titles')
        .then(response => response.json())
        .then(data =>{
            AudioView.displayData(AudioController.parseToAudioObj(data));
            loading.destroy();
        });      
    }

    static parseToAudioObj(data){
        const entries = Object.entries(data);
        console.log(data);
        let list = [];
        let i = 0;
        entries.forEach((element) => {
            let audioobj = element[1];
            list[i] = new AudioModel(audioobj.id,audioobj.title, audioobj.artists, audioobj.album, audioobj.track_lenght);
            i++;
        });
        return list
    }

}

AudioController.getAllTitles();