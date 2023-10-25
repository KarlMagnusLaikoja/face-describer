<template>
    <h1>{{description}}</h1>
</template>

<script>
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});

export async function describe(event){
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
  name: 'DescriptionComponent',
    data() {
        return {
            description: ''
        }
    },
    methods: {
        describe
    }
}
</script>

