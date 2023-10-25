<template>
<div class="gallery EN">
    <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
</div>
<div class="main EE">
    <h1>galerii</h1>
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
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  },
  data() {
            return {
                images: ['estonianFlag.png', 'britishFlag.png'
                , 'estonianFlag.png', 'estonianFlag.png', 'estonianFlag.png', 'estonianFlag.png','estonianFlag.png', 'estonianFlag.png'
                ]
            }
        }
}
</script>