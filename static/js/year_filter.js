function yearFilter(year) {
	var year = document.getElementById("year").value;
	var table = document.getElementById("sort_table");
	
	rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
    	rows[i].type = 'hidden';
    	if (rows[i].getElementsByTagName("TD")[4] == year) {
    		rows[i].type = '';
    	}
    }
}
