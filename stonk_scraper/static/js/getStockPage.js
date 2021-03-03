function getIndividualTicker(tickerInput){
	var ticker = tickerInput;
	var elementWidth = document.getElementById("chartDiv").clientWidth
	if(ticker === null || ticker === "" ){
		console.log("empty")
		return
	}
	document.getElementById("tradingViewTitle").innerHTML = "<h2>" + ticker + " price chart";
	new TradingView.widget(
                {
                  "width": elementWidth,
                  "height": document.getElementById("chartDiv").clientHeight,
                  "symbol": ticker,
                  "interval": "H",
                  "timezone": "Etc/UTC",
                  "theme": "light",
                  "style": "1",
                  "locale": "en",
                  "toolbar_bg": "#f1f3f6",
                  "enable_publishing": false,
                  "allow_symbol_change": true,
                  "container_id": "tradingview_874ba"
                  }
                );
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