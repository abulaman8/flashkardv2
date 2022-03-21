<template>
  <div class="body">
      <div class="box">
          <form @submit.prevent="login">
            <label for="username">Username:</label>
            <input type="text" v-model="username" name="username" required>

            <label for="password">Password:</label>
            <input type="password" v-model="password" name="password" required>

            <center>
                <button type="submit">Log in</button>

            </center>
            
          </form>

      </div>
  </div>
</template>

<script>
export default {
    name: 'Login',
    data(){
        return {
            username: '',
            password: '',
            // data : {
            //     "username": this.username,
            //     "password": this.password
            // }
        }
    },
    methods : {
        login : function login() {
            
            let data = {
                "username": this.username,
                "password": this.password
            }
			// body...
			
			fetch(
				"http://localhost:5000/login",
				{
				method: "POST",
				body: JSON.stringify(data),
				headers:{
					"Content-Type":"application/json",
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
        background-color: grey;
        color: white;
        padding: 10px;
        margin: 20px;
        border-radius: 20px;
        border: none;
        min-width: 200px;
    }
</style>