<template>
<div id = "header">
<TabMenu :model="pages" id="pages"/>
<router-view />
<div id= "languages">
<Avatar image="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flag_of_Estonia.svg/255px-Flag_of_Estonia.svg.png" id="estonian" shape="circle" />
<Avatar image="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Flag_of_the_United_Kingdom_%281-2%29.svg/1200px-Flag_of_the_United_Kingdom_%281-2%29.svg.png" id="english" shape="circle" />
</div>
</div>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
              return {
                  pages: [
                      {label: 'Home', icon: 'pi pi-fw pi-home', to: '/'},
                      {label: 'Face-Describer', icon: 'pi pi-fw pi-cog', to: '/'},
                      {label: 'Contact', icon: 'pi pi-fw pi-phone', to: '/'},
                      {label: 'Gallery', icon: 'pi pi-fw pi-images', to: '/'}
                  ]
              }
          },
}
</script>
