<template>
<div class="main EN">
    <h1>gallery</h1>
</div>
<div class="main EE">
    <h1>galerii</h1>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
export default {
  name: 'Gallery',
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  }
}
</script>