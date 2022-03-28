<template>
  <div class="backdrop" @click.self="closeModal">
      <div class="modal">
          <!-- <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Ratione esse, cumque tempora ullam reiciendis alias molestias, pariatur rem accusantium nihil ut quae eius doloremque minima dolorum tempore reprehenderit eos vero debitis et aliquid natus sequi quasi! Incidunt quaerat eligendi recusandae non ratione quos labore? Voluptates soluta distinctio quibusdam atque voluptatum similique tempore facilis quis modi odio assumenda aut iusto nesciunt in repudiandae, qui dolorum praesentium molestias? Tempora excepturi dolores quod adipisci cumque quis, dolorum ex vero doloribus. In ad deserunt enim eaque illo quae eum fugiat quis quibusdam aut ipsum veritatis ratione corporis quod facere, recusandae, nesciunt perferendis dolore suscipit!</p> -->
           <form @submit.prevent="addDeck" method="POST" enctype='multipart/form-data'>
            <label for="csvfile">Select File:</label>
            <input type="file" @change="addDeck( $event )" name="csvfile" required>


            <center>
                <button type="submit">Import Deck</button>

            </center>
            
          </form>
      </div>
  </div>
</template>

<script>
export default {
    methods: {
        closeModal(){
            this.$emit('close')
            console.log('closing')
        },
        addDeck(e){
            this.$emit('importdeck')
            console.log('add emitted')
            let file = e.target.files[0];
            console.log(file)
            let formData = new FormData();


            
            formData.append( 'csvfile', file );

            fetch(
				"http://localhost:5000/import",
				{
				method: "POST",
				body: formData,
				headers:{
					"Content-Type":"multipart/form-data",
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