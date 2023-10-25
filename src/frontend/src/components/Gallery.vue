<template>
<div class="main EN">
    <h1>gallery</h1>
    <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
</div>
<div class="main EE">
    <h1>galerii</h1>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
import Description from './Description.vue'

export default {
  name: 'Gallery',
  components: {
      Description
  },
  mounted () {
    renderLanguage(this.$store.state.languageCode);
    //Describe images in gallery
    /*for (let i = 0; i < this.$refs.images.length; i++){
        this.$refs.images[i].describe();
    }*/
  },
  data() {
            return {
                images: ['estonianFlag.png', 'estonianFlag.png']
            }
        }
}
</script>