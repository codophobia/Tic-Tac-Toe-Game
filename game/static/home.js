var c = 0;
var flag;
function chance(id) //passing the first player information to view
{	
	if(id == 10) {
		c = 2;
	}
	else {
		c = 1;
	}
    flag = 0;
	var i;
	for(i = 1; i <= 9; i++) {
		var y = document.getElementById(i);
		y.value = "";
	}
	document.getElementById("result").innerHTML = "";
	$.ajax({
		url:"/chance/",
		type:"POST",
		data:{chance:c},
		cache:false,
		success:function(json) {
			if(c == 1) {
				var x = document.getElementById(json['val']);
				x.value = 'X';
			}
			else {
				document.getElementById("result").innerHTML = "START THE GAME";
			}
		},
		error:function(json) {
			alert("error");
		}
	});
}
function change(x,y,id) //passing the user choice or move to view and updating the computer's move
{   
    var y = document.getElementById(id);
    if(c == 1 && flag == 0) {
    	y.value = '0';
        document.getElementById("result").innerHTML = "";
    }
    else if(c == 2 && flag == 0) {
    	y.value = 'X';
        document.getElementById("result").innerHTML = "";
    }
    if(c != 0 && flag == 0) {
    $.ajax({
        url:"/handler/",
        type:"POST",
        data:{pos:id},
        cache:false,
        success:function(json) {
        	if(c == 1) {
        		if(json['res'] == 1) {
        			if(json['winner'] == 'comp') {
        				y = document.getElementById(json['val']);
        				y.value = 'X';
        				document.getElementById("result").innerHTML = "YOU LOST";
                        flag = 1;
        			}
        			else if(json['winner'] == 'player') {
        				document.getElementById("result").innerHTML = "YOU WON";
                        flag = 1;
        			}
        			else {
        				y = document.getElementById(json['val']);
        				y.value = 'X';
        				document.getElementById("result").innerHTML = "GAME DRAW";
                        flag = 1;
        			}
        		}
        		else {
        			y = document.getElementById(json['val']);
        			y.value = 'X';
        		}
        	}
        	else {
        		if(json['res'] == 1) {
        			if(json['winner'] == 'comp') {
        				y = document.getElementById(json['val']);
        				y.value = 'O';
        				document.getElementById("result").innerHTML = "YOU LOST";
                        flag = 1;
        			}
        			else if(json['winner'] == 'player') {
        				document.getElementById("result").innerHTML = "YOU WON";
                        flag = 1;
        			}
        			else {
        				document.getElementById("result").innerHTML = "GAME DRAW";
                        flag = 1;
        			}
        		}
        		else {
        			y = document.getElementById(json['val']);
        			y.value = 'O';
        		}
        	}
        },
        error:function(json) {
            alert(json['val']);
        }
    });
}
}
