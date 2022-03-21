<template>
  <div class="backdrop" @click.self="closeModal">
      <div class="modal">
          <!-- <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Ratione esse, cumque tempora ullam reiciendis alias molestias, pariatur rem accusantium nihil ut quae eius doloremque minima dolorum tempore reprehenderit eos vero debitis et aliquid natus sequi quasi! Incidunt quaerat eligendi recusandae non ratione quos labore? Voluptates soluta distinctio quibusdam atque voluptatum similique tempore facilis quis modi odio assumenda aut iusto nesciunt in repudiandae, qui dolorum praesentium molestias? Tempora excepturi dolores quod adipisci cumque quis, dolorum ex vero doloribus. In ad deserunt enim eaque illo quae eum fugiat quis quibusdam aut ipsum veritatis ratione corporis quod facere, recusandae, nesciunt perferendis dolore suscipit!</p> -->
           <form @submit.prevent="addCard">
            <label for="front">Front:</label>
            <input type="text" v-model="front" name="front" required>
            
            <label for="back">Back:</label>
            <input type="text" v-model="back" name="back" required>


            <center>
                <button type="submit">Add Deck</button>

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
        addCard(){
            this.$emit('addcard')
            console.log('add emitted')
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
    }
    .backdrop{
        top: 0;
        position:fixed;
        background: rgba(0, 0, 0, 0.5);
        width: 100%;
        height: 100%;

        }
</style>