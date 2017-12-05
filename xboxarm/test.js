var fetch = require ('node-fetch');
var url = "https://freegeoip.net/json/";
var lolo = async url => {
   try {
     const response = await fetch(url);
     const json = await response.json();
    console.log(json.ip);
} catch (error) {
    console.log(error);
}};
lolo(url);
