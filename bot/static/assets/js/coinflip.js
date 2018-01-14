var call = 1;
function flip() {
	var decider = Math.floor(Math.random()*100); 
	var coin = document.getElementById("coin");
	//coin.style.transform = "rotateX(50deg)";
	coin.style.transition = "transform 3.5s linear";
	console.log(decider);
	if(decider%2==0){
	coin.style.transform = "rotateX("+call*3650+"deg)";//please adjust the angle
	}
	else{
		coin.style.transform = "rotateX("+call*(3650+180)+"deg)";//please adjust the angle	
	}
	var coin2 = document.getElementById("movement");
	coin2.style.transition = "top 1.5s linear"		
	coin2.style.top = "10%";
	setTimeout(function(){
		coin2.style.transition = "top 0.5s linear"		
		coin2.style.top = "10%";
		setTimeout(function(){
			coin2.style.transition = "top 1.5s linear"		
			coin2.style.top = "55%";
		},500);
	},1500);
	call++;

}