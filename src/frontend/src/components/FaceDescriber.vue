<template>
<div class="main">
    <h1>describer</h1>
    <image-picker/>
    <description/>
</div>
</template>

<script>
import ImagePicker from './ImagePicker.vue'
import Description from './Description.vue'
export default {
  name: 'FaceDescriber',
  components: {
    ImagePicker,
    Description
  }
}
</script>