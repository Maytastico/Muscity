class AudioModel{
    titleLenghtAsString(){
        const min = this.title_lenght/60;
        const sec = this.title_lenght%60;
        return Math.round(min) +":"+ Math.round(sec);
    }

    constructor(id, title, artists,album, title_lenght){
        this.id = id;
        this.title = title;
        this.artists = artists;
        this.album = album;
        this.title_lenght = title_lenght;
        this.track_lenght = this.titleLenghtAsString();
        this.openEdit = false;
    }

    delete(){
        fetch('http://localhost:5000/api/titles/'+this.id, {
        method: 'DELETE',
        })
        .then(data => {
            console.log('Success:', data);
        });
    }

    put(){
        console.log("hi");
        /* fetch('http://localhost:5000/api/titles/'+this.id, {
        method: 'PUT',
        body: JSON.stringify(rename)
        })
        .then(data => {
            console.log('Success:', data);
        }); */
    }
    
}