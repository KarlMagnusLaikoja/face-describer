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
        description = "Pildil oleval inimesel on %faceShape% nägu ja %skinColour% nahk. Tal on %eyeColour% värvi %eyePlacement%, %eyeShape% silmad ja %noseShape% nina. Tal on %hairColour% juuksed ja %facialHairThickness% %facialHairColour% näokarvad.";

        //Face shape
        const faceShapeMapping = {
            "teemant": "teemandi kujuline",
            "oblong": "oblongi kujuline",
            "ovaal": "ovaali kujuline",
            "ümmargune": "ümmargune",
            "ruut": "ruudu kujuline",
        };
        description = description.replace("%faceShape%", faceShapeMapping[data["üldine"]["näo_kuju"]]);

        //Skin colour
        description = description.replace("%skinColour%", data["üldine"]["naha_värv"]);


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
        if(data["silmad"]["värv_parem"] == data["silmad"]["värv_vasak"]){
            description = description.replace("%eyeColour%", eyeColourMapping[data["silmad"]["värv_parem"]]);
        }
        else{
            description = description.replace("värvi", "").replace("%eyeColour%", "eri värvi (vasak "+data["silmad"]["värv_vasak"]+", parem "+data["silmad"]["värv_parem"]+")")
        }


        //Facial hair
        if(data["näokarvad"]["tihedus"] == "puudub"){
            description = description.replace("%facialHairThickness% %facialHairColour% näokarvad.", "tal puuduvad või on väga õrnad näokarvad.");
        }
        else{
            const facialHairThicknessMapping = {
                "õhuke": "õhukesed",
                "tihe": "tihedad"
            };
            const facialHairColourMapping = {
                "punane": "punased",
                "blond": "blondid",
                "pruun": "pruunid",
                "must": "mustad",
                "hall": "hallid"
            };
            description = description.replace("%facialHairThickness%", "tal on "+facialHairThicknessMapping[data["näokarvad"]["tihedus"]]).replace("%facialHairColour%", facialHairColourMapping[data["näokarvad"]["värv"]]);
        }

        //Nose shape
        if(data["nina"]["kuju"] == "nööpnina"){
             description = description.replace("%noseShape% nina", "nööpnina");
        }
        else if(data["nina"]["kuju"] == "kull/kongus"){
            description = description.replace("%noseShape% nina", "kulli nina/kongus nina");
        }
        else{
            description = description.replace("%noseShape%", data["nina"]["kuju"]);
        }

        //Eye shape
        const eyeShapeMapping = {
            "mandel": "mandlikujulised",
            "ümmargune": "ümmargused",
            "monoliidne": "monoliidsed",
            "alla suunatud": "alla suunatud",
            "üles suunatud": "üles suunatud",
            "varjatud/kapuutsiga": "varjatud/kapuutsiga"
        }
        description = description.replace("%eyeShape%", eyeShapeMapping[data["silmad"]["kuju"]]);

        //Eye placement
        description = description.replace("%eyePlacement%", data["silmad"]["asetus"]);

        //Hair
        if(data["juuksed"]["on_olemas"] == "väär"){
            description = description.replace("Tal on %hairColour% juuksed", "Ta on kiilakas");
        }
        else{
            const hairColourMapping = {
                "punane": "punased",
                "blond": "blondid",
                "pruun": "pruunid",
                "must": "mustad",
                "hall": "hallid"
            };
            description = description.replace("%hairColour%", hairColourMapping[data["juuksed"]["värv"]]);
        }
    }



    if(language == "EN"){
        description = "The person in the picture has a %faceShape% shaped face with %skinColour% skin. They have %eyeColour% %eyePlacement%, %eyeShape% eyes and a %noseShape% nose. They have %hairColour% hair and %facialHairThickness% %facialHairColour% facial hair.";

        //Face shape
        const faceShapeMapping = {
            "diamond": "a diamond shaped",
            "oblong": "an oblong",
            "oval": "an oval",
            "round": "a round",
            "square": "a square",
        };
        description = description.replace("a %faceShape% shaped", faceShapeMapping[data["general"]["face_shape"]]);

        //Skin colour
        description = description.replace("%skinColour%", data["general"]["skin_colour"]);

       //Eye colour
       //Consider case where eyes are different coloured
       if(data["eyes"]["colour_right"] == data["eyes"]["colour_left"]){
                description = description.replace("%eyeColour%", data["eyes"]["colour_right"]);
       }
       else{
            description = description.replace("%eyeColour%", "different coloured (the left is "+data["eyes"]["colour_left"]+", the right is "+data["eyes"]["colour_right"]+")");
       }

       //Facial hair
       if(data["facial_hair"]["thickness"] == "none"){
            description = description.replace("%facialHairThickness% %facialHairColour% facial hair.", "they don't have or have very light facial hair.");
       }
       else{
            description = description.replace("%facialHairThickness%", "they have "+data["facial_hair"]["thickness"]).replace("%facialHairColour%", data["facial_hair"]["colour"]);
       }

       //Nose shape
       if(data["nose"]["shape"] == "East Asian" || data["nose"]["shape"] == "upturned"){
        description = description.replace("a %noseShape%", "an "+data["nose"]["shape"]);
       }
       else{
        description = description.replace("%noseShape%", data["nose"]["shape"]);
       }

       //Eye shape
       description = description.replace("%eyeShape%", data["eyes"]["shape"]);

       //Eye placement
       description = description.replace("%eyePlacement%", data["eyes"]["placement"]);

        //Hair
        if(data["hair"]["has_hair"] == "false"){
            description = description.replace("They have %hairColour% hair", "They are bald");
        }
        else{
            description = description.replace("%hairColour%", data["hair"]["colour"]);
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

