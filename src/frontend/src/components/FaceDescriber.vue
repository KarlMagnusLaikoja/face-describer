<template>
<div>
    <div class = "main EN">
        <h1>Pick an image</h1>
        <FileUpload id="fileUpload" url="/describe" :multiple="false" accept="image/*" :maxFileSize="1000000" uploadLabel="Describe" :customUpload="true" @uploader="setImage" @select="removeImage">
            <template #empty>
                <p>Drag and drop files to here to upload.</p>
                <Message severity="error" id="errorMessageContainer" style="display: none;"><p id="errorMessage"></p></Message>
            </template>
        </FileUpload>
        <description v-if="image" v-bind:image="image"/>
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
}
function removeImage(){
    console.log('here');
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