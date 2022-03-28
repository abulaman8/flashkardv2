<template>
  <center>
        <div class="big">
            
            <div class="cardcontainer">
                <div class="card">
                    <div class="front">{{ this.front }}</div>
                    <div class="back">{{ this.back }}</div>
                </div> 
            </div>
           

            <form method="POST" name="autoform" @submit.prevent="next">    
                <div class="rating">
                    
                    <input @click="next(10, this.front, this.back, this.id)" type="radio" name="score" id="rata5" value="10" ><label for="rata5">Jiffy Bezos</label>
                    <input @click="next(8, this.front, this.back, this.id)" type="radio" name="score" id="rata4" value="8" ><label for="rata4">Easy</label>
                    <input @click="next(6, this.front, this.back, this.id)" type="radio" name="score" id="rata3" value="6" ><label for="rata3">Normal</label>
                    <input @click="next(4, this.front, this.back, this.id)" type="radio" name="score" id="rata2" value="4" ><label for="rata2">Hard</label>
                    <input @click="next(2, this.front, this.back, this.id)" type="radio" name="score" id="rata1" value="2" ><label for="rata1">Enigma</label>

                </div>
            </form>

            </div>   
        </center>
</template>

<script>
export default {
  data(){
    return{
      
    }
  },
  props:{
    front:String,
    back:String,
    id:Number
  },
  methods:{
    next(score, front, back, id){
      console.log('next', score, front, back, id)
      this.$emit('next', score, front, back, id)
    }
  }



}
</script>

<style scoped>
.cardcontainer {
	
	height: 300px;
	width: 600px;
	border: 2px solid gray;
	overflow: hidden;
	display: flex;
	justify-content: center;
	margin-top: 40px;
  background: #dddddd;
  z-index: 0;

}

.card {
    /* position: absolute; */
    width: 600px;
    height: 300px;
    transition: all 0.75s ease;
    transform-style: preserve-3d;
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
    font-size: 4em;
    /*box-shadow: 10px 10px 5px 0px rgba(0,0,0,0.3);*/
  }
  
  .front {
    background-color: #333;
    color: #fff;
  }
  
  .back {
    transform: rotateX(180deg);
  
    background-color: #fff; 
    color: #333;
  }

  .btn-group-lg .btn{
  	margin-right: 0px;
  	margin-left: 0px;
  	max-width: 200px;
  	margin-top: 10px;

}
.big {
	border-radius: 10px;
	background-color: ghostwhite;
	border: 2px solid black;
	justify-content: center;
	margin-top: 40px;
	min-height: 500px;
	max-width: 800px;
}

.left {
	float: left;
	margin-top: 25px;
	margin-left: 30px;
}

.right {
	float: right;
	margin-top: 10px;
	margin-right: 30px;
}

        .rating {
            max-height: 55px;
            margin-top: 5%;
            /* border: 1px #999 solid; */
            display: flex;
            font-size:0;
            justify-content: center;
            align-items: center;
            flex-direction: row-reverse;
            background: linear-gradient(to right, #f00 , #ff0, #0f0)
        }
        .rating input {
            display: none
        }
        .rating label {
            display: flex;
            padding: 8px;
            min-width: 125px;
            height: 50px;
            font-size: 21px;
            justify-content: center;
            align-items: center;
            background: #fff;
            color: #000;
          cursor: pointer;
        }
        .rating label {
            border-left: none;
            transition: .3s;
        }
        .rating input[type='radio']:hover~label,
input[type='radio']:checked~label{
            background: none;
            color: #fff;
        }

</style>