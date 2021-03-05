function getSupportedSubs(){
    let promise = fetch("/stock/supportedSubs/")
        promise.then(response => {
                response.json().then(data =>{
                    var subs = data["supportedSubs"];
                    for(let i = 0; i < subs.length; i++){
                        document.getElementById("selectBarStream").innerHTML = document.getElementById("selectBarStream").innerHTML +
                         "<option value=" + subs[i] + ">" +subs[i] + "</option>"; 
                        document.getElementById("selectBar").innerHTML = document.getElementById("selectBar").innerHTML +
                         "<option value=" + subs[i] + ">" +subs[i] + "</option>"; 
                    }
                })
            })

}

function getTickerOverTime(){
    var e = document.getElementById("InputBox");
    var strTicker = e.value;
    var e = document.getElementById("mentionGraphTime");
    var days = e.value;
    var secs = days*60*60*24;
    let promise = fetch("/stock/" + strTicker + "/time/" + secs)
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
            var ctx = document.getElementById('myChart').getContext('2d');
            ctx.visibility = "visible"
            var chart = new Chart(ctx, {
                // The type of chart we want to create
                type: 'line',

                // The data for our dataset
                data: {
                    labels: time,
                    datasets: [{
                        label: strTicker,
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        fill:false,
                        data: mentions
                     }]
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
        })
    })
}

function getSubOverTimeStream(){
    //alert("implement me")
    //TODO: Implement this visually to not look as bad 
    var time = document.getElementById("mentionGraphTimeStream").value*60*60*24;
    var sub = document.getElementById("selectBarStream").value;
    if(sub === "0"){
        alert("Implement error handling")
    }
    if(time === "0"){
        alert("Implement error handling")        
    }
    console.log(time);
    console.log(sub);
    var url = "/subs/" + sub + "/time/" + time;
    let promise = fetch(url)
    promise.then(response => {
        response.json().then(data => {
            document.getElementById("StockTrendStream").innerHTML = "";
            for(var key in data){
                console.log(key)
                document.getElementById("StockTrendStream").innerHTML += "Scan " + key + "<br>"; 
                for (var i = 0; i < data[key].length; i ++){
                    document.getElementById("StockTrendStream").innerHTML += (i+1) + "." + data[key][i][0] + " " + data[key][i][1] + "<br>"; 
                }
            }
        })
    })

}

function getLastUpdate(){
    let promise = fetch("/lastUpdate")
        promise.then(response => {
                response.json().then(data =>{
                    document.getElementById("Time Since").innerHTML = "(" + data["timeInMinutes"] +" minutes ago)";
                    document.getElementById("Time Since2").innerHTML = "(" + data["timeInMinutes"] +" minutes ago)";
                    document.getElementById("Time Since1").innerHTML = "(" + data["timeInMinutes"] +" minutes ago)";
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
                            + ". <a href=\"/stock/" + subs[i][0] +"/page\">"+ subs[i][0] + "</a> " + subs[i][1] + " " + subs[i][2];
                    }
                    console.log(document.getElementById("Stock Results").innerHTML);
                })
            })
}