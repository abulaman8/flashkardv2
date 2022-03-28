<template>
  
  <button @click="toggle">Add Deck</button>
  <button @click="toggleImport">Import deck</button>
  <div v-if="showModal" class="adddeck">
    <AddDeckModal @close="toggle" @adddeck="addDeck" />
  </div>

  
  <div v-if="showImport" class="import">
    <ImportModal @close="toggleImport" @addcard="toggleImport" />
  </div>
  <div class="tableContainer" style="overflow-x:auto;">
    <center>
    <table v-if="decks.length">
      <!-- <tr>
        <th>Deck Name</th>
        
      </tr> -->
      <div v-for="deck in decks">
        <tr>
          <td class="name">{{ deck.deck_name }}</td>
          <td class="edit"><button @click.prevent="exportDeck(deck.deck_name)">Export</button></td>
          <td class="edit"><button @click.prevent="deckControl(deck.deck_name)" >Edit</button></td>
          <td class="delete"><button @click="deleteDeck(deck.deck_name)">Delete</button></td>
        </tr>
        <hr>

      </div>
      

    </table>
    </center>
  </div>
</template>

<script>

import AddDeckModal from "../components/AddDeckModal.vue";

import ImportModal from "../components/ImportModal.vue"

export default {
    name: "managedeck",


    data(){
    return {
      showModal: false,
      showImport:false,
      decks:[]
    }
  },
  methods: {
    
    toggle: function(){
      this.showModal=!this.showModal

      },

    
    toggleImport: function(){
      this.showImport=!this.showImport
    },
    deckControl(name){
      this.$router.push({name:'DeckControl', params:{name:name}})

    },
    addDeck(name){
      this.showModal=!this.showModal

      fetch(
				"http://localhost:5000/dashboard",
				{
				method: "GET",
				
				headers:{
					"token": localStorage.getItem("token")
				},
				
				}
			).then(function(response) {
				return response.json()
			}).then(data => this.decks=data)


    },
    deleteDeck(name){
      let url = "http://localhost:5000/"+name+"/delete"

      fetch(
				url,
				{
				method: "POST",
				headers:{
          "token": localStorage.getItem("token")
				},
				

				}
			).then(function(response) {
				return response.json()
			}).then((rdata)=> {
				console.log(rdata)
        this.decks = this.decks.filter((i)=>(i.deck_name != name))
        
        
			})
      
    },
    exportDeck(name){
      let url = "http://localhost:5000/export/"+name

      fetch(
				url,
				{
				method: "POST",
				headers:{
          "token": localStorage.getItem("token")
				},
				

				}
			).then(function(response) {
				return response.json()
			}).then(function(rdata) {
				console.log(rdata)
        
			})
      
    },
  },

  mounted(){
    fetch(
				"http://localhost:5000/dashboard",
				{
				method: "GET",
				
				headers:{
					"token": localStorage.getItem("token")
				},
				
				}
			).then(function(response) {
				return response.json()
			}).then(data => this.decks=data)
        
      
    
      },


  components:{
    AddDeckModal,
    ImportModal,

  }

}
</script>

<style>
button{
  cursor: pointer;
}
hr{
  width: 100%;
  background: #C0C0C0;
  height: 1px;
}
table{
  width: 70%;
  /* border: 2px solid grey; */
  margin-left: auto;
  margin-right: auto;
  margin: 20px;
}
.name{
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
  /* border-bottom: 2px solid #C0C0C0; */
}
.edit, .delete{
  
  width: 17%;
  /* border-bottom: 2px solid #C0C0C0; */

}
.edit button{
  background: #2a623d;
  border-radius: 5px;
}
.delete button{
  background: black;
  border-radius: 5px;
}
.edit button:hover, .delete button:hover {
  border: 2px solid #C0C0C0;
}
tr:hover{
  background-color: rgba(42,98,61,0.3);
}

</style>