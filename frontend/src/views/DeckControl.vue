<template>
<button @click="toggle">Add Card</button>


<div v-if="showAddCard" class="addcard">
    <AddCardModal @close="toggle" @addcard="addCard" />
</div>
  

  <div class="tableContainer" style="overflow-x:auto;">
    <center>
    <table v-if="cards.length">
      <!-- <tr>
        <th>Deck Name</th>
        
      </tr> -->
      <div v-for="card in cards">
        <tr :class="{deletecard: (card.delete == 'yes')}">
          <td class="name">{{ card.front }}</td>
          <td class="name">{{ card.back}}</td>
          <td class="edit"><button @click.prevent="editCard" >Edit</button></td>
          <td class="delete"><button @click="deleteCard(card.id)">Delete</button></td>
        </tr>
        <hr>

      </div>
      

    </table>
    <button @click="saveStatus" class="save">Save</button>
    </center>
  </div>
</template>

<script>
import AddCardModal from "../components/AddCardModal.vue";

export default {
    data(){
        return{
            showAddCard:false,
            cards: [],
            postCards:[]
        }
    },
    props:{
        name:String
    },

    components:{
        AddCardModal,
    },
    methods:{
        toggle: function(){
        this.showAddCard=!this.showAddCard
        },
        deleteCard(id){
            this.cards.forEach((i)=>{
                if(i.id == id){
                    i.delete = 'yes'
                    this.postCards.push(i)
                    this.cards = this.cards.filter((i)=>(i.id != id))
                    
                    console.log(i)

                }
                
            })
        },
        addCard(front, back){
          this.postCards.push(
            {
              "front":front,
              "back":back,
              "delete":"no",
              "id":"null"
            }
            
          )
          this.showAddCard=!this.showAddCard
          
        },
        saveStatus(){
        console.log('saving')
        let data = {
            "cards":this.postCards,
            "deck_name":this.name
            }
        let url = "http://localhost:5000/"+ this.name+"/edit"
        fetch(
            url,
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
        }).then(data =>{
            console.log(data)
            })
        
        let url2 = "http://localhost:5000/review/"+ this.name
          fetch(
            url2,
            {
            method: "GET",
            
            headers:{
              "token": localStorage.getItem("token")
            },
            
            }
          ).then(function(response) {
            return response.json()
          }).then(data =>{
                    this.cards=data
                    this.cards.forEach(function(i){
                        i['delete'] = 'no'
                    })
                    console.log(this.cards)
                    })

        },
    },
    
    mounted(){
        console.log(this.name)
        let url = "http://localhost:5000/review/"+ this.name
        fetch(
				url,
				{
				method: "GET",
				
				headers:{
					"token": localStorage.getItem("token")
				},
				
				}
			).then(function(response) {
				return response.json()
			}).then(data =>{
                this.cards=data
                this.cards.forEach(function(i){
                    i['delete'] = 'no'
                })
                console.log(this.cards)
                })
    }

    

    


}
</script>

<style>
.deletecard{
    background: rgba(235,15,40, 0.4);
}
.name{
    width: 25%;
}
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