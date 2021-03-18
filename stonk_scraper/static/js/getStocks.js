function getIndividualTicker(){
	var ticker = document.getElementById("InputBox").value;
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
				document.getElementById("Stock Results").innerHTML = "<a href=\'/stock/"  + ticker + "/page\''> "+ ticker + "</a>: " + data["name"] + "<br>" 
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
				var topMentions = [];
				var topSubs = [];
				for(var i = 0; i < data["top"].length ; i++){
					let res = data["top"][i];
					topSubs.push(res[0]);;
					topMentions.push(res[1]);
				}		
				document.getElementById("Stock Results Subs").innerHTML = "<h2>"  + ticker + " mentions chart by sub</h2>"
				

				var mentions = [];
				var subs = [];
				for(var i = 0; i < data["hot"].length ; i++){
					let res = data["hot"][i];
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