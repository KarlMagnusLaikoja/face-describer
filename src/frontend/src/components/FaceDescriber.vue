<template>
<div>
    <div class = "facedescriber">
        <FileUpload id="filePicker" url="/describe" :multiple="false" uploadIcon="pi pi-fw pi-cog" accept="image/*" :maxFileSize="1000000" uploadLabel="Describe" :customUpload="true" @uploader="setImage" @select="removeImage">
            <template #empty>
                <p id="dragNDrop" class="EN">Drag and drop an image file here to describe it.</p>
                <p id="dragNDrop" class="EE">Lohista pildifail siia selle kirjeldamiseks.</p>
                <description v-if="image && this.$store.state.languageCode=='EN'" v-bind:image="image"/>
                <description v-if="image && this.$store.state.languageCode=='EE'" v-bind:image="image"/>
                <Message severity="error" id="errorMessageContainer" style="display: none;"><p id="errorMessage"></p></Message>
            </template>
        </FileUpload>
    </div>

</div>
</template>

<script>
import Description from './Description.vue'
import {renderLanguage} from './AppHeader.vue';
import {setLabels} from './AppHeader.vue';


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
    setLabels(this.$store.state.languageCode);
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