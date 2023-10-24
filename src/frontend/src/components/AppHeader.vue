<template>
<div id = "header">
<div id = "headerContent">
<TabMenu :model="pages_EN" id="pages" class="EN"/>
<TabMenu :model="pages_EE" id="pages" class="EE"/>
<div id= "languages">
<Avatar id="estonian" shape="circle" v-on:click="updateLanguageCode('EE');pickLanguage('EE');renderLanguage('EE')" size="large"/>
<Avatar id="english" shape="circle" v-on:click="updateLanguageCode('EN');pickLanguage('EN');renderLanguage('EN')" size="large"/>
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
export default {
  name: 'AppHeader',
  data() {
              return {
                  pages_EE: [
                       {label: 'Kodu', icon: 'pi pi-fw pi-home', to: '/'},
                       {label: 'Face-Describer', icon: 'pi pi-fw pi-cog', to: '/face-describer'},
                       {label: 'Kontakt', icon: 'pi pi-fw pi-phone', to: '/contact'},
                       {label: 'Galerii', icon: 'pi pi-fw pi-images', to: '/gallery'}
                  ],
                  pages_EN: [
                      {label: 'Home', icon: 'pi pi-fw pi-home', to: '/'},
                      {label: 'Face-Describer', icon: 'pi pi-fw pi-cog', to: '/face-describer'},
                      {label: 'Contact', icon: 'pi pi-fw pi-phone', to: '/contact'},
                      {label: 'Gallery', icon: 'pi pi-fw pi-images', to: '/gallery'}
                  ],
              }
 },
 methods: {
    renderLanguage,
    pickLanguage,
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
