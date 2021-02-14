function getIndividualTicker(){
	var ticker = document.getElementById("InputBox").value;
	if(ticker === null || ticker === "" ){
		console.log("empty")
		return
	}
	let promise = fetch("stock/" + ticker)
	promise.then(response => {
			response.json().then(data =>{
				document.getElementById("Stock Results").innerHTML = ticker + ": "	+ data[ticker];		
			})
		}

	)
}
function getStockData(){
	//TODO Get the stock data
}