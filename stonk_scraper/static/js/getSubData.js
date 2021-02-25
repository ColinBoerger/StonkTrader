function getSupportedSubs(){
	let promise = fetch("/stock/supportedSubs/")
		promise.then(response => {
				response.json().then(data =>{
					var subs = data["supportedSubs"];
					for(let i = 0; i < subs.length; i++){
						document.getElementById("selectBar").innerHTML = document.getElementById("selectBar").innerHTML +
						 "<option value=" + subs[i] + ">" +subs[i] + "</option>"; 
						console.log(document.getElementById("selectBar").innerHTML);
					}
					console.log(document.getElementById("selectBar").innerHTML);
				})
			})

}

function getTickerOverTime(){
	var e = document.getElementById("InputBox");
	var strTicker = e.value;

	let promise = fetch("/stock/" + strTicker + "/time/90400")
	promise.then(response =>{
		response.json().then(data =>{
			let mentions = []
			let time = []
			console.log(data)
			let data1 = data["data"]
			for (let i = 0; i < data1.length; i++){
				res = data1[i]
				mentions.push(res["numMentions"])
				 time.push(res["created"])
				
			} 
			console.log(mentions)
			console.log(time)
			var ctx = document.getElementById('myChart').getContext('2d');
			var chart = new Chart(ctx, {
    			// The type of chart we want to create
    			type: 'line',

    			// The data for our dataset
    			data: {
        			labels: time,
        			datasets: [{
            			label: 'My First dataset',
            			backgroundColor: 'rgb(255, 99, 132)',
            			borderColor: 'rgb(255, 99, 132)',
            			fill:false,
            			data: mentions//[0, 10, 5, 2, 20, 30, 45]
       				 }]
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
	})
}

function getLastUpdate(){
	let promise = fetch("/lastUpdate")
		promise.then(response => {
				response.json().then(data =>{
					document.getElementById("Time Since").innerHTML = "(" + data["timeInMinutes"] +" minutes ago)";
				})
			}
		)
}

function getSubData(){
	//Use clearbit.com/logo to get company logos
	var e = document.getElementById("selectBar");
	var strSub = e.value;
	console.log(strSub)
	let promise = fetch("/subs/"  +strSub)
		promise.then(response => {
				response.json().then(data =>{
					var subs = data["data"];
					if (subs.length === 0 ){
						document.getElementById("Stock Results").innerHTML = "No results";
						return;
					}

					document.getElementById("Stock Results").innerHTML = "";
					for(let i = 0; i < subs.length; i++){
						document.getElementById("Stock Results").innerHTML = 
							document.getElementById("Stock Results").innerHTML + "<br>" + (i+1)
							+ ". " + subs[i][0] + " " + subs[i][1] + " " + subs[i][2];
					}
					console.log(document.getElementById("Stock Results").innerHTML);
				})
			})
}