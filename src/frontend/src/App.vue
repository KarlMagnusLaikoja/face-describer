<template>
  <app-header/>
  <router-view />
  <app-footer/>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';
import {renderLanguage} from './components/AppHeader.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter
  },
  mounted () {
       renderLanguage(this.$store.state.languageCode);
  }
};
</script>


