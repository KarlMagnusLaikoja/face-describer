<template>
<div class="main EN">
    <h1>contact</h1>
</div>
<div class="main EE">
    <h1>kontakt</h1>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
export default {
  name: 'Contact',
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  }
}
</script>