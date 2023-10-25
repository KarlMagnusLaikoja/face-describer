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
import {describe} from './Description.vue';


export default {
  name: 'ImagePicker',
  methods: {
    describe
  }
}
</script>