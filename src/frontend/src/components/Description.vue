<template>
    <img ref="image"/>
    <p ref="description"></p>
</template>

<script>
async function describe(fileNameOrBase64, language, refs){
    //Get image
    var image;
    if (fileNameOrBase64.startsWith('data')){
        image = fileNameOrBase64;
    }
    else{
        image = require('@/assets/'+fileNameOrBase64);
    }

    //Display image
    refs.image.src = image;

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

    //Propagate any errors to Face-Describer component
    if (response.errorCode != 0){

        if(document.getElementById('errorMessageContainer')){
        document.getElementById('errorMessageContainer').style.display='';
        document.getElementById('errorMessage').innerHTML = response.errorMessage;
        return;
        }
        //No error in Gallery component, just text
        refs.description.innerHTML = "Failed to describe image";
        return;
    }


    //Propagate result, typing effect for aesthetic purposes
    for (let i = 0; i < response.descriptionResult.length; i++){
        if (!refs.description) return; //Hacky fix for when user navigates before the text has been written
        refs.description.innerHTML += response.descriptionResult.charAt(i);
        await new Promise(t => setTimeout(t, 50));
    }

}

export default {
  name: 'DescriptionComponent',
    props: ['image'],
    methods: {
        describe
    },
    mounted(){
        describe(this.image, this.$store.state.languageCode, this.$refs);
    }
  }


</script>

