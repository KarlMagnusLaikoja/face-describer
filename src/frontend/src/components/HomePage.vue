<template>
<div class="home">
    <div class="intro">
        <p>intro</p>
    </div>
    <Divider/>
    <div class="homepage_description EN" v-if="this.$store.state.languageCode=='EN'">
        <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
    </div>
    <div class="homepage_description EE" v-if="this.$store.state.languageCode=='EE'">
        <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
    </div>
    <Divider/>
    <div class="faq">
            <p>intro</p>
    </div>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
import Description from './Description.vue'
export default {
  name: 'HomePage',
  components: {
        Description
  },
  created () {
      //Get first image from gallery
      const galleryFiles = require.context('../assets/gallery', false)
                                  .keys().map(key => key.slice(2))
      this.images.push(galleryFiles[0]);
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