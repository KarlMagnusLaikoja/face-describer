<template>
    <h1>xd</h1>
    <h1>{{image}}</h1>
    <img :src="require(`@/assets/${image}`)"/>
    <p id="description"></p>
</template>

<script>
async function describe(fileName, language){
    //Get image
    const image = require('@/assets/'+fileName);

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

    //Propagate any errors in Face-Describer component
    if (response.errorCode != 0){

        if(document.getElementById('errorMessageContainer')){
        document.getElementById('errorMessageContainer').style.display='';
        document.getElementById('errorMessage').innerHTML = response.errorMessage;
        return;
        }
        //Do not render in Gallery component
        //TODO
        return;
    }


    //Propagate result
    document.getElementById('description').innerHTML = response.descriptionResult;

}

export default {
  name: 'DescriptionComponent',
    props: ['image'],
    methods: {
        describe
    },
    mounted(){
        describe(this.image, this.$store.state.languageCode);
    }
  }


</script>

