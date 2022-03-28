<template>
    

    <Card :front="this.cfront" :back="this.cback" :id="this.cid" @next="nextcard" />
  
</template>

<script>

import Card from "../components/Card.vue"
export default {
    data(){

        return{
            cards:[],
            cfront:'loading...',
            cback:'',
            cid: NaN
        }

    },
    props:{
        name:String,
    },
    methods:{
        nextcard(score, front, back, id){
            console.log('emission recieved')
            console.log(score, front, back, id)

            let f = this.cards.pop()
            this.cards.unshift(f)
            this.cfront=f.front
            this.cback=f.back
            this.cid=f.id
            let data={
                "cards": [
                    {
                        "id":id,
                        "front":front,
                        "back":back,
                        "score":score
                    }
                ]
            }
            let url = "http://localhost:5000/review/"+ this.name
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
            
        }
    },
    components:{
        Card,
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
                let f=this.cards.pop()
                this.cards.unshift(f)
                console.log(f)
                this.cfront=f.front
                this.cback=f.back
                this.cid=f.id
                

                
                })
        

    },
}
</script>

<style>

</style>