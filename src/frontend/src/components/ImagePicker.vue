<template>
<div class = "main EN">
    <h1>Pick an image</h1>
    <FileUpload id="fileUpload" url="/describe" :multiple="false" accept="image/*" :maxFileSize="1000000" uploadLabel="Describe" :customUpload="true" @uploader="describe">
        <template #empty>
            <p>Drag and drop files to here to upload.</p>
            <Message severity="error" id="errorMessageContainer" style="display: none;"><p id="errorMessage">test</p></Message>
        </template>
    </FileUpload>
</div>



<div class = "main EE">
    <h1>Vali pilt</h1>
</div>
</template>

<script>
/*
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});

async function describe(){
    //File to base64
    var image = await toBase64(event.files[0]);
    console.log(image);
*/
export default {
  name: 'ImagePicker',
  methods: {
    describe: function(){
        this.$root.$emit('describe');
    }
  }
}
</script>