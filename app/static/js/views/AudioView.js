Vue.component('list-entry', {
    props: {
        item: AudioModel,
    },
    methods: {
        say: function (message) {
            AudioView.deleteDialog(message)
        }
    },
    template: '<div class="listEntry"><section class="thumbnail"><div><img src="/static/img/example.jpg"></div></section><section class="title">{{item.title}}</section><section class="artists">{{item.artists}}</section><section class="title-lenght">{{item.track_lenght}}</section><section class="button-area"><button class="round red" v-on:click="say(item)"><img src="/static/icons/feather/trash-2.svg"></button><button @click="item.openEdit = true" class="round"><img src="/static/icons/feather/edit-2.svg"></button></section></div>',
});

Vue.component('edit-entry', {
    props: {
        item: AudioModel,
    },
    data: function () {
        return {
            title: "Hi",
            artists: "Miau",
            album: "Hau"
        }
    },
    methods: {
        put: function(item){
            item.put("Hi")
        }
    },
    template: '<section v-if="item.openEdit" @close="item.openEdit = false" class="overlay flex center horizontalCenter open"><div  class="flex center column horizontalCenter"><h2 data-name="feedback" class="flex center">Edit {{ item.title }}</h2><section data-name="inputs" class="center"><input v-model="title" v-bind:placeholder="{item.title}" ><input v-model="artists" v-bind:placeholder="{item.artists}""><input v-model="album" v-bind:placeholder="{item.album}"></section><section data-name="buttons" class="center"><button v-on:click="put(item)" class="highlighted">Commit</button><button @click="$emit(\'close\')">Cancel</button></section></div></section>',
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

    }
}