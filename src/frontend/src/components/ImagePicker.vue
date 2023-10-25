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
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});

async function describe(event){
    //File to base64
    var image = await toBase64(event.files[0]);
    console.log(image);

    //Get language from store
    const language = this.$store.state.languageCode;

    //Send description request to backend
    var response = await fetch("/describe", {
      method: "POST",
      body: JSON.stringify({
        "language": language,
        "image": image
      }),
      headers: {
        "Content-type": "application/json;charset=UTF-8"
      }
    });
    response = await response.json();

    //Propagate any errors
    if (response.errorCode != 0){
        document.getElementById('errorMessageContainer').style.display='';
        document.getElementById('errorMessage').innerHTML = response.errorMessage;
        return;
    }


    //Propagate result to description field
    //TODO
    console.log(response);
}



export default {
  name: 'ImagePicker',
  methods: {
    describe
  }
}
</script>