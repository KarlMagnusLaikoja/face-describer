<template>
<div>
    <div class = "facedescriber">
        <div id="filePicker">
        <h1 class="fdheader EN">Pick an image</h1>
        <h1 class="fdheader EE">Vali pilt</h1>
        <FileUpload url="/describe" :multiple="false" uploadIcon="pi pi-fw pi-cog" accept="image/*" :maxFileSize="10000000" uploadLabel="Describe" :customUpload="true" @uploader="setImage" @select="removeImage">
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
        <WebCamUI :fullscreenButton="{display: false, text: '', css: ''}" @photoTaken="takePhoto"/>
        </div>
        <description v-if="image && this.$store.state.languageCode=='EN'" v-bind:image="image"/>
        <description v-if="image && this.$store.state.languageCode=='EE'" v-bind:image="image"/>
        <Sidebar v-model:visible="infoBarVisible" position="bottom" id="infobar">
                        <div v-if="this.$store.state.languageCode=='EN'" v-html="englishInfoBarText" class="infobardiv"/>
                        <div v-if="this.$store.state.languageCode=='EE'" v-html="estonianInfoBarText" class="infobardiv"/>
        </Sidebar>
        <Button icon="pi pi-info-circle" @click="infoBarVisible = true" label="How is my data processed and how can I get the most accurate results?" class="EN" id = "infobarbutton"/>
        <Button icon="pi pi-info-circle" @click="infoBarVisible = true" label="Kuidas töödeldakse minu andmeid ning kuidas saan ma täpseima tulemuse?" class="EE" id = "infobarbutton"/>
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
                          image: null,
                          infoBarVisible: false,
                          englishInfoBarText: "<h1>How is my data processed?</h1><h3><a href = 'https://gdpr-info.eu' target='_blank'>General Data Protection Regulation</a> categorises images of human faces as biometric data.</h3><p>Facedescriber's workflow requires input images to be temporarily saved on disk. All inputted images are deleted at the end of the program's work and are not retained in any way.</p><u>By using Facedescriber I confirm that I am aware of my data's usage and necessity.</u><h1>How can I get the most accurate results?</h1><h3>1. Face directly toward the camera with a neutral expression.</h3><p>Keep your eyes open, mouth closed and your face parallel to the camera.</p><h3>2. Achieve standard, uniform lighting.</h3><p>No bright lights or shadows being cast on the face.</p><h3>3. Do not wear any accessories.</h3><p>No hats, glasses or facial coverings.</p>",
                          estonianInfoBarText: "<h1>Kuidas töödeldakse minu andmeid?</h1><h3><a href = 'https://gdpr-info.eu' target='_blank'>Isikuandmete kaitse üldmäärus</a> kategoriseerib pildi inimese näost biomeetriliste andmete hulka.</h3><p>Facedescriberi töövoog nõuab sisendpildi ajutist salvestamist kettale. Kõik sisestatud pildid kustutakse rakenduse töö lõpus ära ning ei jäädvustata mingil moel.</p><u>Kasutades Facedescriberit kinnitan, et olen teadlik minu isikuandmete kasutusest ja tarvilikkusest.</u><h1>Kuidas saan ma täpseima tulemuse?</h1><h3>1. Vaata otse kaamera poole neutraalse ilmega.</h3><p>Hoia silmad lahti, suu kinni ja nägu paralleelselt kaamera suhtes.</p><h3>2. Saavuta tavaline, ühtlane valgustus.</h3><p>Näo peale ei tohiks langeda varje või väga eredat valgust.</p><h3>3. Ära kanna aksessuaare.</h3><p>Eemalda mütsid, prillid ja näokatted.</p>"
                      }
      },
  methods: {
    setImage,
    removeImage,
    takePhoto
  }
}
</script>