<template>
  <div class="backdrop" @click.self="closeModal">
      <div class="modal">
          <!-- <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Ratione esse, cumque tempora ullam reiciendis alias molestias, pariatur rem accusantium nihil ut quae eius doloremque minima dolorum tempore reprehenderit eos vero debitis et aliquid natus sequi quasi! Incidunt quaerat eligendi recusandae non ratione quos labore? Voluptates soluta distinctio quibusdam atque voluptatum similique tempore facilis quis modi odio assumenda aut iusto nesciunt in repudiandae, qui dolorum praesentium molestias? Tempora excepturi dolores quod adipisci cumque quis, dolorum ex vero doloribus. In ad deserunt enim eaque illo quae eum fugiat quis quibusdam aut ipsum veritatis ratione corporis quod facere, recusandae, nesciunt perferendis dolore suscipit!</p> -->
           <form @submit.prevent="addDeck">
            <label for="deckname">Deck Name:</label>
            <input type="text" v-model="deckname" name="deckname" required>


            <center>
                <button type="submit">Create Deck</button>

            </center>
            
          </form>
      </div>
  </div>
</template>

<script>
export default {

    data(){
        return{
            deckname:''
        }
            
        
    },
    methods: {
        closeModal(){
            this.$emit('close')
            console.log('closing')
        },
        addDeck(e){
            this.$emit('adddeck', this.deckname)
            console.log(this.deckname)
            console.log('add emitted')
            let data = {
                "deck_name":this.deckname,
                "cards":[]
            }
            fetch(
				"http://localhost:5000/create-deck",
				{
				method: "POST",
				body: JSON.stringify(data),
				headers:{
					"Content-Type":"application/json",
                    "token": localStorage.getItem("token")
				},
				

				}
			).then(function(response) {
				return response.json()
			}).then(function(rdata) {
				console.log(rdata)
			})
        }
    }

}
</script>

<style scoped>
    .modal{
        width: 400px;
        padding: 20px;
        margin: 100px auto;
        background: white;
        border-radius: 10px;
        text-align: left;
        z-index: 15;
        position: absolute;
        transform-style: preserve-3d;
        top: 10%;
        left: 30%;
    }
    .backdrop{
        top: 0;
        position:fixed;
        background: rgba(0, 0, 0, 0.5);
        width: 100%;
        height: 100%;

        }
</style>