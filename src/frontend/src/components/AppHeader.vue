<template>
<div id = "header">
<div id = "headerContent">
<TabMenu :model="pages_EN" id="pages" class="EN"/>
<TabMenu :model="pages_EE" id="pages" class="EE"/>
<div id= "languages">
<Avatar image="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flag_of_Estonia.svg/255px-Flag_of_Estonia.svg.png" id="estonian" shape="circle" v-on:click="updateLanguageCode('EE');renderLanguage('EE')"/>
<Avatar image="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Flag_of_the_United_Kingdom_%281-2%29.svg/1200px-Flag_of_the_United_Kingdom_%281-2%29.svg.png" id="english" shape="circle" v-on:click="updateLanguageCode('EN');renderLanguage('EN')"/>
</div>
</div>
</div>
</template>

<script>
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
                  ]
              }
 },
 methods: {
    renderLanguage,
    updateLanguageCode: function (languageCode) {
        this.$store.dispatch('updateLanguageCode', languageCode)
    }
    }
 }
</script>
