<template>
<div class = "descriptionContainer">
    <Image>
        <template #image>
            <img ref="image" class="image"/>
        </template>
    </Image>
    <Panel ref="panel" class="description" header="Description" toggleable>
        <p  ref="description"/>
    </Panel>
</div>
<Divider/>
</template>

<script>
async function describe(fileNameOrBase64, language, refs){
    //Set english or estonian headers for descriptions
    setDescriptionHeaders(language);

    //Get image
    var image;
    if (fileNameOrBase64.startsWith('data')){
        image = fileNameOrBase64;
    }
    else{
        image = require('@/assets/gallery/'+fileNameOrBase64);
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
        propagateError(response, refs, language);
        return;
    }
    response = await response.json();

    //Propagate any errors to Face-Describer component
    if (response.errorCode != 0){
        propagateError(response, refs, language);
    }


    //Propagate result, typing effect for aesthetic purposes
    for (let i = 0; i < response.descriptionResult.length; i++){
        if (!refs.description) return; //Hacky fix for when user navigates before the text has been written
        refs.description.innerHTML += response.descriptionResult.charAt(i);
        await new Promise(t => setTimeout(t, 50));
    }

}

function propagateError(response, refs, language){
    var errorText = response.status==500?
                        language=="EN"?
                            "Failed to describe image":
                             "Kirjeldamine ebaõnnestus"
                        :response.errorMessage;
    if(document.getElementById('errorMessageContainer')){
            document.getElementById('errorMessageContainer').style.display='';
            document.getElementById('errorMessage').innerHTML = errorText;
            refs.image.style.display = 'none'; //Do not display image on failure to describe
            return;
    }
    //No error in Gallery component, just text
    refs.description.innerHTML = errorText;
}

function setDescriptionHeaders(languageCode){
    var headers = document.getElementsByClassName('p-panel-title');
    for (let i = 0; i < headers.length; i++){
        headers[i].innerHTML = languageCode == "EN" ?
                                    "Description":
                                    "Kirjeldus";
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
    },
    data() {
        return {

        }
      }
  }


</script>

