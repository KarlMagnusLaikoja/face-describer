<template>
<div class="home EN">
    <h1>homepage</h1>
    <Divider/>
    <h1>x</h1>
</div>
<div class="home EE">
    <h1>koduleht</h1>
    <Divider/>
    <h1>x</h1>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
export default {
  name: 'HomePage',
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  }
}
</script>