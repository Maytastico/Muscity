Vue.component('list-entry', {
    props: {
        item: AudioModel,
    },
    methods: {
        deleteEntry: function (message) {
            AudioView.deleteDialog(message)
        },
        edit: function (message){
            AudioView.editDialog(message);
        }
    },
    template: '<div class="listEntry"><section class="thumbnail"><div><img :src="item.thumbnail"></div></section><section class="title">{{item.title}}</section><section class="artists">{{item.artists}}</section><section class="title-lenght">{{item.track_lenght}}</section><section class="button-area"><button class="round red" v-on:click="deleteEntry(item)"><img src="/static/icons/feather/trash-2.svg"></button><button v-on:click="edit(item)" class="round"><img src="/static/icons/feather/edit-2.svg"></button></section></div>',
});

document.querySelector("#addTrack").addEventListener("click", () => {
    let addView =  new Dialog({
        generateOverlay: true,
        feedbackMsg: `Add new Track`,
        generateButtonContainer: true,
        generateInputContainer: true,
        open: true
    });
    

    let titleInput = addView.addInput('editTitle',{
        placeholder: "Title",
    });

    let artistsInput = addView.addInput('editArtist',{
        placeholder: "Artist",
    });
    
    let albumInput = addView.addInput('editAlbum',{
        placeholder: "Album",
    });

    let trackLenghtInput = addView.addInput('trackLenghtInput',{
        placeholder: "Tracklenght in seconds",
        type: "number",
    });

    addView.addButton("editEntry", {
        "msg": "Add"
    }).addEventListener("click", () => {
        let index = 3;
        if(titleInput.value.length < 1){
            addView.addMessage("ErrorTitle", "A new entry needs a title", ["notify", "alert"]);
            index--;
        }
        if(artistsInput.value.length < 1){
            addView.addMessage("ErrorTitle", "A new entry needs an artist", ["notify", "alert"]);
            index--;
        }
        if(albumInput.value.length < 1){
            addView.addMessage("ErrorTitle", "A new entry needs an album",  ["notify", "alert"]);
            index--;
        }
        if(index == 3){
            let newAudioObj = new AudioModel(null, titleInput.value, artistsInput.value, albumInput.value, trackLenghtInput.value)
            self.audioData.push(newAudioObj)
            newAudioObj.add();
            let success = new Dialog({
                generateOverlay: true,
                feedbackMsg: `Added successfully`,
                type: "check",
                close: {action:"destroy"},
                open: true
            })
        }
        
    });

    addView.addButton("editEntry", {
        "msg": "Close",
        additionalClasses: ['highlighted']
    }).addEventListener("click", () => {
        console.log("canceled");
        addView.destroy();
    });
});

class AudioView {
    static audioData;

    static displayData(incomingAudioData) {
        console.log(incomingAudioData)
        self.audioData = incomingAudioData;
        var audioView = new Vue({

            el: '#audioView',
            data: {
                items: self.audioData,
                showEdit: false
            },


        });
    }

    static deleteDialog(audioobj) {
        let deleteDialog = new Dialog({
            generateOverlay: true,
            feedbackMsg: `Do you really want to delete ${audioobj.title}?`,
            generateButtonContainer: true
        });
        deleteDialog.addButton("deleteEntry", {
            "additionalClasses": ["red"],
            "msg": "Delete"
        }).addEventListener("click", () => {
            audioobj.delete();
            console.log(self.audioData);
            for (let i = 0; i < self.audioData.length; i++) {
                if (self.audioData[i].id == audioobj.id) {
                    self.audioData.splice(i, 2);
                    break;
                }
            }
            deleteDialog.destroy();
        });
        deleteDialog.addButton("Cancel", {
            "msg": "Cancel"
        }).addEventListener("click", () => {
            deleteDialog.destroy();
        });
        deleteDialog.open();
    }

    static editDialog(audioobj) {
        let editView =  new Dialog({
            generateOverlay: true,
            feedbackMsg: `Edit ${audioobj.title}`,
            generateButtonContainer: true,
            generateInputContainer: true,
            open: true
        });
        

        let titleInput = editView.addInput('editTitle',{
            value: audioobj.title,
        });

        let artistsInput = editView.addInput('editArtist',{
            value: audioobj.artists,
        });
        
        let albumInput = editView.addInput('editAlbum',{
            value: audioobj.album,
        });

        editView.addButton("editEntry", {
            "msg": "Edit"
        }).addEventListener("click", () => {
            let toEdit = []
            let idOfElement = 0
            for (let i = 0; i < self.audioData.length; i++) {
                if (self.audioData[i].id == audioobj.id) {
                    idOfElement = i;
                    break;
                }
            }   
            if(titleInput.value.length > 1){
                toEdit.push({tilte: titleInput.value}) ;
                self.audioData[idOfElement].title = titleInput.value;
            }
            if(artistsInput.value.length > 1){
                toEdit.push({artists: artistsInput.value}) ;
                self.audioData[idOfElement].artists = artistsInput.value;
            }
            if(albumInput.value.length > 1){
                toEdit.push({album: albumInput.value});
                self.audioData[idOfElement].album = albumInput.value;
            }
            if(audioobj.title != self.audioData[idOfElement].title || audioobj.title != self.audioData[idOfElement].artists || audioobj.album != self.audioData[idOfElement].album){
                self.audioData[idOfElement].update();
                let success = new Dialog({
                    generateOverlay: true,
                    feedbackMsg: `Edited ${self.audioData[idOfElement].title} successfully`,
                    type: "check",
                    close: {action:"destroy"},
                    open: true
                })
            }
            
        });

        editView.addButton("editEntry", {
            "msg": "Close",
            additionalClasses: ['highlighted']
        }).addEventListener("click", () => {
            console.log("canceled");
            editView.destroy();
        });

        
    }
}