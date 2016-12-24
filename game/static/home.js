var c = 0;
var board = [0,0,0,0,0,0,0,0,0];
var flag = -1;
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
    document.getElementById("result").innerHTML = "";
	for(i = 1; i <= 9; i++) {
		var y = document.getElementById(i);
		y.value = "";
	}
    for(var i = 0; i < board.length; i++) {
        board[i] = 0;
    }
    if(c == 1) {
        var x = Math.floor(Math.random() * 8);
        board[x] = 1;
        document.getElementById(x+1).value = 'X';
    }
    else {
        document.getElementById("result").innerHTML = "START THE GAME";
    }
}
function change(xpos,ypos,id) //passing the user choice or move to view and updating the computer's move
{   
    var y = document.getElementById(id);
    var index = 3*parseInt(xpos)+parseInt(ypos);
    if(c == 1) {
        if(y.value == "") {
    	   y.value = '0';
           board[index] = 2;
        }
    }
    else if(c == 2) {
        if(y.value == ""){
    	   y.value = 'X';
           board[index] = 2;
        }
    }
    if(c) {
        document.getElementById("result").innerHTML = "";
        $.ajax({
            url:"/handler/",
            type:"POST",
            data:{"board[]":board},
            cache:false,
            success:function(json) {
            	if(c == 1) {
            		if(json['res'] == 1) {
            			if(json['winner'] == 'comp') {
            				y = document.getElementById(json['val']+1);
            				y.value = 'X';
            				document.getElementById("result").innerHTML = "YOU LOST";
            			}
            			else if(json['winner'] == 'player') {
            				document.getElementById("result").innerHTML = "YOU WON";
            			}
            			else {
            				y = document.getElementById(json['val']+1);
            				y.value = 'X';

            				document.getElementById("result").innerHTML = "GAME DRAW";
            			}
                        c = 0;
            		}
            		else {
            			y1 = document.getElementById(json['val']+1);
                        board[parseInt(json[['val']])] = 1;
            			y1.value = 'X';
            		}
            	}
            	else {
            		if(json['res'] == 1) {
            			if(json['winner'] == 'comp') {
            				y = document.getElementById(json['val']+1);
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
                        c = 0;
            		}
            		else {
            			y1 = document.getElementById(json['val']+1);
            			y1.value = 'O';
                        board[parseInt(json[['val']])] = 1;
            		}
            	}
            },
            error:function(json) {
                alert(json['val']);
            }
        });
    }
}
