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
    if (response.errorCode && response.errorCode != 0){
        try{
        propagateError(response, refs, language);
        } catch (error){
        //Ignore exception, error refs will load eventually
        }
        return;
    }
    else if (response.veakood && response.veakood != 0){
        try{
            propagateError(response, refs, language);
        } catch (error){
            //Ignore exception, error refs will load eventually
        }
        return;
    }


    //Propagate result
    compileAndPropagateResult(response, refs, language);
}

async function compileAndPropagateResult(response, refs, language){
    var description = "";
    const data = language == "EE" ? response.kirjeldus : response.description;

    if(language == "EE"){
        description = "Pildil oleval inimesel on %faceShape% nägu ja %skinColour% nahk. Tal on %eyeColour% värvi silmad. Tal on %facialHairThickness% %facialHairColour% näokarva kate.";

        //Face shape
        const faceShapeMapping = {
            "teemant": "teemandi kujuline",
            "oblong": "oblongi kujuline",
            "ovaal": "ovaali kujuline",
            "ümmargune": "ümmargune",
            "ruut": "ruudu kujuline",
        };
        description = description.replace("%faceShape%", faceShapeMapping[data["näo kuju"]]);

        //Skin colour
        description = description.replace("%skinColour%", data["naha värv"]);


        //Eye colour
        const eyeColourMapping = {
            "sinine": "sinist",
            "pruun": "pruuni",
            "roheline": "rohelist",
            "hall": "halli",
            "pähkelpruun": "pähkelpruuni",
            "punane": "punast"
        }

        //Consider case where eyes are different coloured
        if(data["parema silma värv"] == data["vasaku silma värv"]){
            description = description.replace("%eyeColour%", eyeColourMapping[data["parema silma värv"]]);
        }
        else{
            description = description.replace("värvi", "").replace("%eyeColour%", "eri värvi (vasak "+data["vasaku silma värv"]+", parem "+data["parema silma värv"]+")")
        }


        //Facial hair
        if(data["näokarvade tihedus"] == "puudub"){
            description = description.replace("Tal on %facialHairThickness% %facialHairColour% näokarva kate.", "Tal puudub või on väga õrn näokarva kate.");
        }
        else{
            description = description.replace("%facialHairThickness%", data["näokarvade tihedus"]).replace("%facialHairColour%", data["näokarvade värv"]);
        }
    }



    if(language == "EN"){
        description = "The person in the picture has a %faceShape% shaped face with %skinColour% skin. They have %eyeColour% eyes. They have %facialHairThickness% %facialHairColour% facial hair.";

        //Face shape
        description = description.replace("%faceShape%", data["face shape"]);

        //Skin colour
        description = description.replace("%skinColour%", data["skin colour"]);

       //Eye colour
       //Consider case where eyes are different coloured
       if(data["right eye colour"] == data["left eye colour"]){
                description = description.replace("%eyeColour%", data["right eye colour"]);
       }
       else{
            description = description.replace("%eyeColour%", "different coloured (the left is "+data["left eye colour"]+", the right is "+data["right eye colour"]+")");
       }

       //Facial hair
       if(data["facial hair thickness"] == "none"){
            description = description.replace("They have %facialHairThickness% %facialHairColour% facial hair", "They don't have or have very light facial hair.");
       }
       else{
            description = description.replace("%facialHairThickness%", data["facial hair thickness"]).replace("%facialHairColour%", data["facial hair colour"]);
       }
    }



    //Typing effect for aesthetic purposes
    for (let i = 0; i < description.length; i++){
        if (!refs.description) return; //Hacky fix for when user navigates before the text has been written
        refs.description.innerHTML += description.charAt(i);
        await new Promise(t => setTimeout(t, 50));
    }
}

function propagateError(response, refs, language){
    var errorText = response.status==500?
                        language=="EN"?
                            "Failed to describe image":
                             "Kirjeldamine ebaõnnestus"
                        :language=="EN"?
                            response.errorMessage:
                            response.veateade
                        ;
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

