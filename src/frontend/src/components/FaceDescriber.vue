<template>
<div>
    <image-picker/>
    <description/>
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
  }
}
</script>