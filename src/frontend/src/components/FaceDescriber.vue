<template>
<div class="main EN">
    <h1>describer</h1>
    <image-picker/>
    <description/>
</div>
<div class="main EE">
    <h1>kirjeldaja</h1>
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