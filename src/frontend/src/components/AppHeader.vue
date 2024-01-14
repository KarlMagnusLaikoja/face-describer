<template>
<div id = "header">
<div id = "headerContent">
<TabMenu :model="pages_EN" id="pages" class="EN"/>
<TabMenu :model="pages_EE" id="pages" class="EE"/>
<div id= "languages">
<Avatar id="estonian" shape="circle" v-on:click="updateLanguageCode('EE');pickLanguage('EE');renderLanguage('EE');setLabels('EE')" size="large"/>
<Avatar id="english" shape="circle" v-on:click="updateLanguageCode('EN');pickLanguage('EN');renderLanguage('EN');setLabels('EN')" size="large"/>
</div>
</div>
</div>
</template>

<script>
import estonianFlag from "../assets/estonianFlag.png";
import britishFlag from "../assets/britishFlag.png";
export function renderLanguage(languageCode){
        const elements_EE = document.getElementsByClassName('EE');
        const elements_EN = document.getElementsByClassName('EN');
        if (languageCode == 'EN'){
            //Hide EE
            for (let i = 0; i < elements_EE.length; i++){
                elements_EE[i].style.display = 'none';
            }
            //Reveal EN
            for (let i = 0; i < elements_EN.length; i++){
                elements_EN[i].style.display = '';
            }
            return;
        }
        //languageCode == 'EE'
        for (let i = 0; i < elements_EN.length; i++){
            elements_EN[i].style.display = 'none';
        }
        for (let i = 0; i < elements_EE.length; i++){
            elements_EE[i].style.display = '';
        }
}
function pickLanguage(languageCode){
    if (languageCode == 'EN'){
        document.getElementById('estonian').style.border = 'transparent';

        document.getElementById('english').style.border = '';
        document.getElementById('english').style.borderStyle = 'solid';
        document.getElementById('english').style.borderColor = 'green';
        return;
    }
    //languageCode == 'EE'
    document.getElementById('english').style.border = 'transparent';

    document.getElementById('estonian').style.border = '';
    document.getElementById('estonian').style.borderStyle = 'solid';
    document.getElementById('estonian').style.borderColor = 'green';
}
export function setLabels(languageCode){
    var labels = document.getElementsByClassName('p-button-label');
    if(languageCode=="EN"){
        for (let i = 0; i < labels.length; i++){
            switch(labels[i].innerHTML){
                case "Vali":
                    labels[i].innerHTML = "Choose";
                    break;
                case "Kirjelda":
                    labels[i].innerHTML = "Describe";
                    break;
                case "Tühista":
                    labels[i].innerHTML = "Cancel";
                    break;
            }
        }
        return;
    }
    //languageCode=="EE"
        for (let i = 0; i < labels.length; i++){
            switch(labels[i].innerHTML){
                case "Choose":
                    labels[i].innerHTML = "Vali";
                    break;
                case "Describe":
                    labels[i].innerHTML = "Kirjelda";
                    break;
                case "Cancel":
                    labels[i].innerHTML = "Tühista";
                    break;
            }
        }
}
export default {
  name: 'AppHeader',
  data() {
              return {
                  pages_EE: [
                       {label: 'Kodu', icon: 'pi pi-fw pi-home', to: '/'},
                       {label: 'Facedescriber', icon: 'pi pi-fw pi-cog', to: '/face-describer'},
                       //{label: 'Kontakt', icon: 'pi pi-fw pi-phone', to: '/contact'},
                       {label: 'Galerii', icon: 'pi pi-fw pi-images', to: '/gallery'}
                  ],
                  pages_EN: [
                      {label: 'Home', icon: 'pi pi-fw pi-home', to: '/'},
                      {label: 'Facedescriber', icon: 'pi pi-fw pi-cog', to: '/face-describer'},
                      //{label: 'Contact', icon: 'pi pi-fw pi-phone', to: '/contact'},
                      {label: 'Gallery', icon: 'pi pi-fw pi-images', to: '/gallery'}
                  ],
              }
 },
 methods: {
    renderLanguage,
    pickLanguage,
    setLabels,
    updateLanguageCode: function (languageCode) {
        this.$store.dispatch('updateLanguageCode', languageCode)
    }
    },
 mounted () {
    //Set images programmatically
    document.getElementById('estonian').innerHTML = '<img src="'+estonianFlag+'" data-pc-section="image">';
    document.getElementById('english').innerHTML = '<img src="'+britishFlag+'" data-pc-section="image">';

    //Pick chosen language
    pickLanguage(this.$store.state.languageCode);
 }
 }
</script>
