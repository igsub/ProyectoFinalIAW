import Vue from 'vue';
import App from './App.vue';
import router from './router';
import * as VueGoogleMaps from 'vue2-google-maps';

Vue.config.productionTip = false;

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCuncF_e4EWbWLxUygp-5ljmvny_DmItLs',
    libraries: 'places' // necessary for places input
  }
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
