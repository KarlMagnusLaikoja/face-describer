<template>
<div class="gallery EN" v-if="this.$store.state.languageCode=='EN'">
    <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
</div>
<div class="gallery EE" v-if="this.$store.state.languageCode=='EE'">
    <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
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
  created () {
    //Get all images in gallery and push them to the array
    const galleryFiles = require.context('../assets/gallery', false)
                                .keys().map(key => key.slice(2)).filter( (file) => file != "homepage.png")
        for (let i = 0; i < galleryFiles.length; i++){
            this.images.push(galleryFiles[i]);
        }
  },
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  },
  data() {
            return {
                images: []
            }
        }
}
</script>