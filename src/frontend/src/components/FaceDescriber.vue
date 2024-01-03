<template>
<div>
    <div class = "facedescriber">
        <div id="filePicker">
        <h1 class="fdheader EN">Pick an image</h1>
        <h1 class="fdheader EE">Vali pilt</h1>
        <FileUpload url="/describe" :multiple="false" uploadIcon="pi pi-fw pi-cog" accept="image/*" :maxFileSize="1000000" uploadLabel="Describe" :customUpload="true" @uploader="setImage" @select="removeImage">
            <template #empty>
                <p id="dragNDrop" class="EN">Drag and drop an image file here to describe it.</p>
                <p id="dragNDrop" class="EE">Lohista pildifail siia selle kirjeldamiseks.</p>
            </template>
        </FileUpload>
        </div>
        <h1 class="fdheader EN m">or</h1>
        <h1 class="fdheader EE m">või</h1>
        <div id="webcam">
        <h1 class="fdheader EN">Use your webcam</h1>
        <h1 class="fdheader EE">Kasuta oma veebikaamerat</h1>
        <WebCamUI :fullscreenButton="{display: false, text: '', css: ''}" @photoTaken="takePhoto" />
        </div>
        <description v-if="image && this.$store.state.languageCode=='EN'" v-bind:image="image"/>
        <description v-if="image && this.$store.state.languageCode=='EE'" v-bind:image="image"/>
    </div>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
import {setLabels} from './AppHeader.vue';
import { WebCamUI } from 'vue-camera-lib';

export const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});
async function setImage(event){
    //File to base64
    this.image = await toBase64(event.files[0]);

    //Needed
    renderLanguage(this.$store.state.languageCode);
}
function removeImage(){
    this.image = null;
}
async function takePhoto(data){
    this.image = null;
    await new Promise(r => setTimeout(r, 500));
    this.image = data.image_data_url;
}


export default {
  name: 'FaceDescriber',
  components: {
    WebCamUI
  },
  mounted () {
    renderLanguage(this.$store.state.languageCode);
    setLabels(this.$store.state.languageCode);
  },
  data() {
          return {
                          image: null
                      }
      },
  methods: {
    setImage,
    removeImage,
    takePhoto
  }
}
</script>