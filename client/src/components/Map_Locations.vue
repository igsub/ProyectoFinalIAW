<template>
  <div>
      <nav class="light-blue lighten-1" role="navigation">
          
          <a id="logo-container" href="#" class="brand-logo center">
            D.h.e.
            <i class="large material-icons">place</i>
          </a>
      </nav>

      <div class="section no-pad-bot" id="index-banner">
        <div class="container">
          <br><br>
          <h1 class="header center orange-text">¿Dónde has estado?</h1>
          <div class="row center">
            <h5 class="header col s12 light">
              Encuentra las ubicaciones de los últimos post de instagram de un usuario o las últimas menciones a un hashtag.
            </h5>
          </div>
          <div class="row center">
            <div class="container">
              <div class="input-field col s12">
                <input id="input" type="text" class="validate" v-model="inputValue">
                <label for="input">Escribe aquí</label>
                <span class="helper-text" data-error="wrong" data-success="right">
                  Escribe un usuario público de instagram o un hashtag de Twitter (sin '#').
                </span>
                <p>
                  <label style="margin:10px;">
                    <input name="group1" type="radio" value="0" v-model="inputType" checked />
                    <span>Usuario de Instagram</span>
                  </label>
                  <label style="margin:10px;">
                    <input name="group1" type="radio" value="1" v-model="inputType" />
                    <span>Hashtag de Twitter</span>
                  </label>
                </p>
                <button v-on:click="removeMarkers"
                  class="btn waves-effect waves-light red"
                  style="margin:5px;">
                  Eliminar Marcadores
                  <i class="material-icons right">delete</i>
                </button>                  
                <button v-on:click="onSubmit"
                  class="btn waves-effect waves-light"
                  type="submit"
                  name="action"
                  style="margin:5px;">
                  Localizar
                  <i class="material-icons right">send</i>
                </button>
              </div>
            </div>
          
          <br><br>
        </div>
        </div>
      </div>
      <h6 class="header center orange-text">{{msg}}</h6>
      <google-map ref="googleMap"/>        
      <div class="footer-copyright orange">
        <div class="container">
          Made by Ignacio Suburu
        </div>
      </div>
  </div>
</template>

<script>
// Importo la libreria que genera los mensajes HTTP hacia el servidor que maneja las consultas.
import axios from 'axios';
// Importo la componente del mapa de google.
import GoogleMap from './GoogleMap';

export default {
  name: 'Map_Locations',
  components: {
    GoogleMap
  },
  data() {
    return {
      msg: '',
      inputValue: '',
      inputType: '',
    };
  },
  methods: {
    getMap() {
      const path = 'http://127.0.0.1:5000/map_locations';
      axios.get(path)
        .then((res) => {
          this.msg = res.data.message;          
          // Update map
          this.$refs.googleMap.update(res.data.markers);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      if (this.controlInputs()){
        const path = 'http://127.0.0.1:5000/map_locations';
        const payload = {
          input: this.inputValue,
          inputType: this.inputType,
        };
        axios.post(path, payload)
          .then(() => {
            this.getMap();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.getMap();
          });
      };
    },
    removeMarkers() {
      this.$refs.googleMap.removeMarkers();
      this.msg = '';
    },
    controlInputs(){
      if(this.inputValue == '' || this.inputType == ''){
        alert('You must fill all input fields.');
        return false;
      }
      else 
        return true;
    }
  },
};
</script>
