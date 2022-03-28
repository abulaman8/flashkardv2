<template>
  


  <!-- <div class="decktest">
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
    <Deck/>
  </div> -->
  <div class="decktest">
    <div  v-for="deck in this.decks">
      <Deck :name="deck.deck_name" :last="deck.lastrev" :score="deck.score" @delete="deleteDeck" />
    </div>
    
 


  </div>

  

  <!-- <div class="cardtest">
    <Card/>
  </div> -->
  
  
</template>

<script>

import Deck from "./Deck.vue";
import Card from "./Card.vue";
export default {
  name: 'HelloWorld',
  
  props: {
    msg: String
  },
  components:{
    Deck,
    Card

  },
  data(){
    return{
      decks:[],
    }
  },
  methods:{
    deleteDeck(name){
      this.decks = this.decks.filter((i)=>(i.deck_name != name))
    }
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
        
      
    
      }
    

  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.decktest{
  /* display: grid;
  grid-template-columns: repeat(autofit, minmax(300px, 1fr)); */
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  /* margin-left: 60px; */
  align-content: center;
  z-index: 0px;
  }
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
