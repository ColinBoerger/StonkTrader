function getIndividualTicker(){
	var ticker = document.getElementById("InputBox").value;
	if(ticker === null || ticker === "" ){
		console.log("empty")
		return
	}
	let promise = fetch("stock/" + ticker)
	promise.then(response => {
			response.json().then(data =>{
				document.getElementById("Stock Results").innerHTML = data["name"] + "<br>" 
				document.getElementById("Stock Results").innerHTML += "Top Mentions - " + ticker + ": "	+ data[ticker + "top"] + "<br>";		
				document.getElementById("Stock Results").innerHTML += "Hot Mentions- " + ticker + ": "	+ data[ticker + "hot"];		
			})
		}

	)
}
function getTickerSubData(){
	var ticker = document.getElementById("InputBox").value;
	if(ticker === null || ticker === "" ){
		console.log("empty")
		return
	}
	let promise = fetch("stock/" + ticker + "/subs")
	promise.then(response => {
			response.json().then(data =>{
				document.getElementById("Stock Results Subs").innerHTML = " Mentions by Sub: <br>Top: <br>"
				for(var i = 0; i < data["top"].length ; i++){
					let res = data["top"][i];
					document.getElementById("Stock Results Subs").innerHTML += res[0] + " " + res[1] + "<br>"
				}	
				document.getElementById("Stock Results Subs").innerHTML += "Hot: <br>"
				for(var i = 0; i < data["hot"].length ; i++){
					let res = data["hot"][i];
					document.getElementById("Stock Results Subs").innerHTML += res[0] + " " + res[1] + "<br>"
				}	
			})
		}

	)
}