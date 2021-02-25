function getIndividualTicker(){
	var ticker = document.getElementById("InputBox").value;
	var elementWidth = document.getElementById("Stock Results").clientWidth
	if(ticker === null || ticker === "" ){
		console.log("empty")
		return
	}
	new TradingView.widget(
                {
                  "width": elementWidth,
                  "height": 610,
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
				var topMentions = [];
				var topSubs = [];
				for(var i = 0; i < data["top"].length ; i++){
					let res = data["top"][i];
					document.getElementById("Stock Results Subs").innerHTML += res[0] + " " + res[1] + "<br>"
					topSubs.push(res[0]);;
					topMentions.push(res[1]);
				}		
				document.getElementById("Stock Results Subs").innerHTML += "Hot: <br>"
				

				var mentions = [];
				var subs = [];
				for(var i = 0; i < data["hot"].length ; i++){
					let res = data["hot"][i];
					document.getElementById("Stock Results Subs").innerHTML += res[0] + " " + res[1] + "<br>"
					subs.push(res[0]);;
					mentions.push(res[1]);
				}

            	document.getElementById("chartDiv").innerHTML = "<canvas id=\"myChartHot\" display=\"inline-block\";></canvas>"
				var ctx = document.getElementById('myChartHot').getContext('2d');
            	ctx.visibility = "visible"
            	var chart = new Chart(ctx, {
                	// The type of chart we want to create
                	type: 'bar',

                	// The data for our dataset
                	data: {
                    	labels: subs,
                    	datasets: [{
                        	label: 'Top',
                        	backgroundColor: 'rgb(0, 99, 132)',
                        	borderColor: 'rgb(0, 99, 132)',
                        	fill:false,
                        	data: topMentions
                     	},{
                        	label: "Hot",
                        	backgroundColor: 'rgb(255, 99, 132)',
                        	borderColor: 'rgb(255, 99, 132)',
                        	fill:false,
                        	data: mentions
                     	}
                     	]
                	},

                	// Configuration options go here
               	 	options: {        
                    	scales: {
                        	y: {
                            	beginAtZero: true
                            	}
                    	}
                	}
            	});	
			})
		}

	)
}