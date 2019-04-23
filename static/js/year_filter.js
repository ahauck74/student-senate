function yearFilter() {
	var year = document.getElementById("year").value;
	var table = document.getElementById("sort_table");
	
	var rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length); i++) {
    	rows[i].style = 'display:none'; 
    	if (rows[i].getElementsByTagName("TD")[4].innerText == year) {
    		rows[i].style = '';
    	}
    }
}
