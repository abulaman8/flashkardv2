<template>
  <nav>
    <router-link to="/">FlashBoard</router-link> |
    <router-link to="/about">About</router-link> | 
    <router-link :to="{name: 'Login'}">Login</router-link> | 
    <router-link :to="{name: 'Register'}">Register</router-link> | 
    <router-link :to="{name: 'Manage'}">Manage Decks</router-link>
  </nav>
  <router-view/>
</template>

<style>
body{
  --primaryGreen: #1a472a;
  --secondaryGreen: #2a623d;
  --primaryGrey: #5d5d5d;
  --secondaryGrey: #dddddd;
  --black: 	#000000;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  align-content: center;
  /* color: var(--secondaryGrey);
  background: var(--secondaryGrey); */
}

nav {
  padding: 30px;
  
}

nav a {
  font-weight: bold;
  color: var(--primaryGreen);
  text-decoration: none;
  padding: 10px;
  margin-top: 10px auto;
  
}

nav a.router-link-exact-active {
  min-height: 20px;
  color: white;
  background-color: var(--primaryGreen);
  border-radius: 3px;
  text-decoration: none;
}
</style>
