<template>
<div class = "descriptionContainer">
    <Image>
        <template #image>
            <img ref="image" class="image"/>
        </template>
    </Image>
    <Panel class="description" header="Description" toggleable>
        <p  ref="description"/>
    </Panel>
</div>
<Divider/>
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
    if(response.status==500){ //Backend error
        propagateError(response, refs);
    }
    response = await response.json();

    //Propagate any errors to Face-Describer component
    if (response.errorCode != 0){
        propagateError(response, refs);
    }


    //Propagate result, typing effect for aesthetic purposes
    for (let i = 0; i < response.descriptionResult.length; i++){
        if (!refs.description) return; //Hacky fix for when user navigates before the text has been written
        refs.description.innerHTML += response.descriptionResult.charAt(i);
        await new Promise(t => setTimeout(t, 50));
    }

}

function propagateError(response, refs){
    var errorText = response.status==500? "Failed to describe image" : response.errorMessage;
    if(document.getElementById('errorMessageContainer')){
            document.getElementById('errorMessageContainer').style.display='';
            document.getElementById('errorMessage').innerHTML = errorText;
            refs.image.style.display = 'none'; //Do not display image on failure to describe
    }
    //No error in Gallery component, just text
    refs.description.innerHTML = errorText;
    return;
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

