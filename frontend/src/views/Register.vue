<template>
  <div class="body">
      <div class="box">
          <form @submit.prevent="register">


            <label for="email">Email:</label>
            <input type="email" name="email" v-model="email" required>

            <label for="username">Username:</label>
            <input type="text" name="username" v-model="username" required>

            <label for="password">Password:</label>
            <input type="password" name="password" v-model="password" required>

            <center>
                <button type="submit">Sign up</button>

            </center>
            
          </form>

          <p>{{ email }}</p>
          <p>{{ username }}</p>
          <p>{{ password }}</p>

      </div>
  </div>
  
</template>

<script>

export default {
    name: 'Register',
    data(){
        return {
            email: '',
            username: '',
            password: '',
            data : {
                "email": this.email,
                "username": this.username,
                "password": this.password
            }
        }
    },
    methods : {
        register : function(){

            fetch(
                'http://127.0.0.1:5000/register',
                {
                    method : 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(
                        {
                            "username": this.username,
                            "password": this.password,
                            "email": this.email
                        }
                    )
                }
                

                
                ).then(function(response) {
				return response.json()
			}).then(function(rdata) {
				console.log(rdata)
			})
            

        }
    },
    

}
</script>

<style>


    body{
        width: 100%;
        background-color: #eee;
    }
    .box{
        max-width: 420px;
        margin: 30px auto;
        background-color: white;
        text-align: left;
        padding: 40px;
        border-radius: 10px;
    }
    label{
        letter-spacing: 1px;
        color: #aaa;
        margin: 25px 0 15px;
        text-transform: uppercase;
        font-weight: bold;
        display: inline-block;
    }
    input{
        display: block;
        padding: 10px 6px;
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-bottom: 1px solid #ddd;
        color: #555;

    }
    button{
        background-color: #2a623d;
        color: white;
        padding: 10px;
        margin: 20px;
        border-radius: 20px;
        border: none;
        min-width: 200px;
    }

</style>