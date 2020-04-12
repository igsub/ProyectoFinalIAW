import Vue from 'vue';
import VueRouter from 'vue-router';
import MapLocations from '../components/Map_Locations.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/map_locations',
    name: 'Map_Locations',
    component: MapLocations,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
