class AudioModel{
    titleLenghtAsString(){
        const min = this.title_lenght/60;
        const sec = this.title_lenght%60;
        return Math.round(min) +":"+ Math.round(sec);
    }

    constructor(id=null, title, artists,album, title_lenght){
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

    update(){
        let rename = {
            title: this.title,
            artists: this.artists,
            album: this.album
        }
        let form_data = new FormData();

        for ( let key in rename ) {
            form_data.append(key, rename[key]);
        }
        fetch('http://localhost:5000/api/titles/'+this.id, {
            method: 'PUT',
            body: form_data
        })
        .then(data => {
            console.log('Success:', data);
        });
    }

    add(){
        console.log("added");
    }
    
}