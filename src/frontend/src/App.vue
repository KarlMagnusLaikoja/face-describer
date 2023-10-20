<template>
  <app-header/>
  <router-view />
  <app-footer/>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter
  },
  mounted () {
       //Hide EE by default
       const elements_EE = document.getElementsByClassName('EE');
       for (let i = 0; i < elements_EE.length; i++){
          elements_EE[i].style.display = 'none';
       }
  }
};
</script>


