class AudioModel{
    titleLenghtAsString(){
        const title_lenght = Math.round(this.title_lenght)
        const min = Math.round(title_lenght/60);
        const sec = title_lenght%60;
        console.log(sec);
        return min +":"+ sec;
    }

    constructor(id=null, title, artists,album, title_lenght, file_name){
        this.id = id;
        this.title = title;
        this.artists = artists;
        this.album = album;
        this.title_lenght = title_lenght;
        this.track_lenght = this.titleLenghtAsString();
        this.file_name =  file_name;
        this.thumbnail = "/static/img/cover/" + file_name + ".jpg";
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