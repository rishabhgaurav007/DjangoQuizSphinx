var total_second = 10;
	var c_minutes = parseInt(total_second/60);
	var c_seconds = parseInt(total_second%60);
	function CheckTime() {
		document.getElementById("quiz-time-left").innerHTML
		= 'Time Left :' + c_minutes + ' minutes ' + c_seconds + ' seconds ';

		if (total_second <= 0)
		{
			setTimeout('document.quiz.submit()',1);
			//url_mask = $( "#test" ).html()
		}
		else
		{
			total_second = total_second -1;
			c_minutes = parseInt(total_second/60);
			c_seconds = parseInt(total_second%60);
			setTimeout("CheckTime()",1000);
		}

	}
	setTimeout("CheckTime()",1000);