<template>
  <div class= "container">
        <div class="card">
            <div class="front">{{ this.name }}</div>
            <div class="back">
                <ul>
                    <li> score: {{ this.score }}</li>
                    <li> last rev. time: {{ this.last }}</li>
                </ul>
                
                <div class="btn-group" role="group">
                    <a href="#" @click.prevent="manage(this.name)" class="btn btn-outline-dark">Manage</a>
                    <a href="#" @click.prevent="reviewDeck(this.name)" class="btn btn-outline-dark">Review</a>
                    <a href="#" @click.prevent="exportDeck(this.name)" class="btn btn-outline-dark">Export</a>
                    <a href="#" @click.prevent="deleteDeck(this.name)" class="btn btn-outline-dark">Delete</a>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
export default {
  

  props:{
    name: String,
    last: String,
    score: Number
  },
  methods:{
    manage(name){
      this.$router.push({name: 'DeckControl', params:{name:name}})
    },
    reviewDeck(deckname){
      this.$router.push({name: 'Review', params:{name:deckname}})
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
			}).then(function(rdata) {
				console.log(rdata)
        
			})

      this.$emit('delete', name)
      
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
  }

}
</script>

<style scoped>
a{
    /* border: 2px black; */
    color: white;
    background: #2a623d;
    margin: 2px;
    padding: 7px;
    font-size: 0.7em;
    /* border-radius: 5px; */
    text-decoration: none;
    height: 35px;
    width: 60px;
    
    
    
}
a:hover{
  border: 2px solid #C0C0C0;
}
.card {
    margin: 20px;
    /* position: absolute; */
    width: 290px;
    height: 210px;
    max-width: 100%;
    transition: all 0.75s ease;
    transform-style: preserve-3d;
    border-radius: 5px;
    text-align: center;
  }
  
  .card:hover {
    transform: rotateX(180deg);
  }
  
  .front, .back {
    /* This part controls the flip */
    backface-visibility: hidden;
    
    /* Size and card position */
    position: absolute;
    width: 100%;
    height: 100%;
  
    /* Appearance */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 1.5em;
    box-shadow: 10px 10px 5px 0px rgba(42,98,61,0.8);
  }
  
  .front {
    
    background-color: #63d471;
    background-image: linear-gradient(315deg, #63d471 0%, #233329 74%);

    
    
    color: #000;
  }
  
  .back {
    transform: rotateX(180deg);
    text-align: left;
  
    background-color: #fff; 
    color: #333;
  }

</style>