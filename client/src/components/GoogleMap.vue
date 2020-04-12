<template>
  <div>
    <gmap-map
      :center="center"
      :zoom="2.9"
      style="width:100%;  height: 800px;">
      <gmap-marker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        :animation="m.animation"
        :icon="m.icon"
        v-on:click="center=m.position">
      </gmap-marker>
    </gmap-map>
  </div>
</template>

<script>
export default {
  name: "GoogleMap",
  data() {
    return {
      center: { lat: 0, lng: 0 },
      markers: [],
    };
  },
  mounted() {
    this.geolocate();
  },
  methods: {
    geolocate: function() {
      navigator.geolocation.getCurrentPosition(position => {
        this.center = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      });
    },
    update: function (newmarkers) {
      newmarkers.forEach(element => {
        this.markers.push({ 
          position: element,
          animation: google.maps.Animation.DROP,
        });
      });
    },
    removeMarkers: function () {
      this.markers = [];
    }
  }
};
</script>
