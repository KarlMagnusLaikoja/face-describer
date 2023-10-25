<template>
<div>
    <div class = "main EN">
        <h1>Pick an image</h1>
        <FileUpload id="filePicker" url="/describe" :multiple="false" uploadIcon="pi pi-fw pi-cog" accept="image/*" :maxFileSize="1000000" uploadLabel="Describe" :customUpload="true" @uploader="setImage" @select="removeImage">
            <template #empty>
                <p id="dragNDrop">Drag and drop files to here to upload.</p>
                <description v-if="image" v-bind:image="image"/>
                <Message severity="error" id="errorMessageContainer" style="display: none;"><p id="errorMessage"></p></Message>
            </template>
        </FileUpload>
    </div>



    <div class = "main EE">
        <h1>Vali pilt</h1>
    </div>

</div>
</template>

<script>
import Description from './Description.vue'
import {renderLanguage} from './AppHeader.vue';

const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});
async function setImage(event){
    //File to base64
    this.image = await toBase64(event.files[0]);

    //Hide the drag n drop text
    document.getElementById('dragNDrop').innerHTML = '';
}
function removeImage(){
    this.image = null;
}

export default {
  name: 'FaceDescriber',
  components: {
    Description
  },
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  },
  data() {
          return {
                          image: null
                      }
      },
  methods: {
    setImage,
    removeImage
  }
}
</script>