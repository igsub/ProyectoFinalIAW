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
    /** 
    Metodo que se acciona al presionar el boton de localizar y que genera un mensaje HTTP GET hacia el servidor de python para obtener la lista de coordenadas y luego actualizar el mapa.
    */
    getMap() {
      // Direccion del servidor python.
      const path = 'http://127.0.0.1:5000/map_locations';
      // GET
      axios.get(path)
        .then((res) => {
          // Obtiene el mensaje de la respuesta y lo muestra en la pagina.
          this.msg = res.data.message;          
          // Actualiza el mapa con la lista de coordenadas obtenida.
          this.$refs.googleMap.update(res.data.markers);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    /**
     * Metodo que genera un mensaje HTTP POST hacia el servidor de python, con el contenido de los datos ingresados por el usuario.
    */
    onSubmit(evt) {
      evt.preventDefault();
      if (this.controlInputs()){
        // Direccion del servidor python.
        const path = 'http://127.0.0.1:5000/map_locations';
        // Datos ingresados por el usuario.
        const payload = {
          input: this.inputValue,
          inputType: this.inputType,
        };
        // POST
        axios.post(path, payload)
          .then(() => {
            // Luego de finalizado el mensaje POST, realiza un GET para obtener la lista de coordenadas generada.
            this.getMap();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.getMap();
          });
      };
    },
    /**
     * Metodo que se acciona al presionar el boton de remover marcadores y dispara el metodo de la componente GoogleMap para vaciar la lista de marcadores.
     */
    removeMarkers() {
      this.$refs.googleMap.removeMarkers();
      this.msg = '';
    },
    /**
     * Metodo de control para que lo ingresado por el usuario no sea vacio.
     */
    controlInputs(){
      if(this.inputValue == '' || this.inputType == ''){
        alert('Debe completar todos los campos para poder localizar.');
        return false;
      }
      else 
        return true;
    }
  },
};
</script>
