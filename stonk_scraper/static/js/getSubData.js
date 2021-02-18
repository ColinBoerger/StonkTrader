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