function getIndividualTicker(tickerInput){
	var ticker = tickerInput;
	var elementWidth = document.getElementById("chartDiv").clientWidth
	if(ticker === null || ticker === "" ){
		console.log("empty")
		return
	}
	document.getElementById("tradingViewTitle").innerHTML = "<h2>" + ticker + " price chart </h2>";
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
	let promise = fetch("/stock/" + ticker);
	promise.then(response => {
			response.json().then(data =>{
				document.getElementById("Stock Results").innerHTML = data["name"] + "<br>" 
				document.getElementById("Stock Results").innerHTML += "Top Mentions - " + ticker + ": "	+ data[ticker + "top"] + "<br>";		
				document.getElementById("Stock Results").innerHTML += "Hot Mentions- " + ticker + ": "	+ data[ticker + "hot"];		
			})
		}

	);
	console.log("here");
	let promise2 = fetch("/stock/subs/" + ticker );
	console.log("here");
	promise2.then((response => {
			response.json().then(data =>{
				var res = {}
				let scans = []
				console.log(data);
				for(var k in data["results"]){
					let sub = data["results"][k]["subReddit"];
					let numMnetions = data["results"][k]["numMentions"];
					let scan = data["results"][k]["scan"];
					if(scans.indexOf(scan) < 0 ){
						scans.push(scan)
					}
					if(res[sub]){
						res[sub][scan] = numMnetions;
					} else {
						res[sub] = {}
						res[sub][scan] = numMnetions;
					}
				}
				for(var s in scans){
					for(var sub in res){
						if(res[sub][s]){
							console.log(s)
						} else {
							res[sub][s] = 0
						}
					}
				}
				console.log(res);
				console.log(scans);
				document.getElementById("MentionsPerSub").innerHTML = "<h2>Mentions by sub over time</h2>"
				document.getElementById("chartDiv").innerHTML = "<canvas id=\"myChartTrend\" display=\"inline-block\";></canvas>"
				var ctx = document.getElementById('myChartTrend').getContext('2d');
            	ctx.visibility = "visible";
            	var chart = new Chart(ctx, {
                	// The type of chart we want to create
	                type: 'line',

	                // The data for our dataset
	                data: {
	                    labels: scans,
	                    datasets: []
	                },

	                // Configuration options go here
	                options: {        
	                    scales: {
	                       yAxes: [{
	                            ticks: {
	                                beginAtZero: true
	                            }
	                        }]
	                    }
	                }
            	});
            	for(let sub in res){
            		let toEdit = []
            		for(var i in scans){
            			i = scans[i];
            			toEdit.push(res[sub][i]);
            		}
            		let color = getRandomColor();
            		dataPointToAdd = {
            			label:sub,
            			fill:false,
            			data:toEdit,
            			backgroundColor:color,
            			borderColor:color
            		}
            		chart.data.datasets.push(dataPointToAdd);
            	}
            	chart.update();
			})
		}

	));
}

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    console.log(color)
    return color;
}