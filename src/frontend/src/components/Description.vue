<template>
<div class = "descriptionContainer">
    <Image>
        <template #image>
            <img ref="image" class="image"/>
        </template>
    </Image>
    <Panel ref="panel" class="description" header="Description" toggleable>
        <p  ref="description"/>
        <div ref="errorMessageContainer" style="display: none;">
        <Message severity="error"><p ref="errorMessage"></p></Message>
        </div>
    </Panel>
</div>
<Divider/>
</template>

<script>
import {toBase64} from './FaceDescriber.vue';

async function describe(fileNameOrBase64, language, refs){
    //Set english or estonian headers for descriptions
    setDescriptionHeaders(language);

    //Get image
    var image;
    if (fileNameOrBase64.startsWith('data')){
        image = fileNameOrBase64;
    }
    else{
        image = require('@/assets/gallery/'+fileNameOrBase64); //name
        image = await fetch(image);
        image = await image.blob();

        //Convert to base64
        image = await toBase64(image);
    }

    //Display image
    try{
    refs.image.src = image;
    } catch (error){
        //Ignore exception, image ref will load eventually
    }

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
        try{
        propagateError(response, refs, language);
        } catch (error){
        //Ignore exception, error refs will load eventually
        }
        return;
    }
    response = await response.json();

    //Propagate any errors to field
    if (response.errorCode != 0){
        try{
        propagateError(response, refs, language);
        } catch (error){
        //Ignore exception, error refs will load eventually
        }
        return;
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
    refs.errorMessageContainer.style.display='';
    refs.errorMessage.innerHTML = errorText;
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

