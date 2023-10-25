<template>
<div>
    <image-picker/>
    <description v-bind:image="image" v-bind:description="description"/>
        <h1>{{image}}</h1>
        <h1>{{description}}</h1>
</div>
</template>

<script>
import ImagePicker from './ImagePicker.vue'
import Description from './Description.vue'
import {renderLanguage} from './AppHeader.vue';
export default {
  name: 'FaceDescriber',
  components: {
    ImagePicker,
    Description
  },
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  },
  data() {
          return {
              image: '1',
              description: '2'
          }
      }
}
</script>