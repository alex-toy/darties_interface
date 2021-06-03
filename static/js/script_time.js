function get_load_date(year, monthIndex) {
    const load_date = new Date(year, monthIndex);
    return load_date
}



function get_delta() {
    var year = document.getElementById("year_select").value;
    const today = new Date()
    const current_year = today.getFullYear();

    delta = current_year - year

    return delta
}



function get_html_months() {

    maybeObject = document.getElementById("month_select_cumul");

    if (typeof maybeObject != 'object') {
        maybeObject.innerHTML = "";
     }
    
    delta = get_delta();
    const current_month = today.getMonth() + 1;

    var html = '<select class="myforms" name="mois" id="mois_select">'
    const month_list = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre'];

    var option_prev = '<option value="'
    var option_next = '</option>'

    var i;
    var init = 0;
    if(delta < 2){
        html += '<option value="1|janvier">--Choix du mois--</option>'
    } else {
        var init = current_month;
        html += option_prev + init + '|' + month_list[current_month] + '">--Choix du mois--' + option_next;
    }
    
    for (i = init; i < month_list.length; i++) { 
        month_int = i + 1
        html += option_prev + month_int + '|' + month_list[i] + '">' +  month_list[i] + option_next;
    }
    
    html += '</select>'

    document.getElementById("month_select").innerHTML = html;
}




function get_html_years() {
    const current_year = today.getFullYear();

    var html = '<select style="width:150px;height:30px" name="mois" id="mois-select">'
    var option_prev = '<option value="'
    var option_next = '</option>'

    var i;
    for (i = current_year-2; i < 2; i++) { 
        html += option_prev + i + '">' +  i + option_next;
    }
    
    html += '</select>'

    document.getElementById("month_select").innerHTML = html;
}



function get_html_all_months() {

    maybeObject = document.getElementById("month_select");

    if (typeof maybeObject != 'object') {
        maybeObject.innerHTML = "";
     }
    
    var html = '<select class="myforms" name="mois_cumul" id="mois-select" style="padding:0px;" >'
    const month_list = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre'];

    var option_prev = '<option value="'
    var option_next = '</option>'

    var i;
    for (i = 0; i < month_list.length; i++) { 
        month_int = i + 1
        html += option_prev + month_int + '|' + month_list[i] + '">' +  month_list[i] + option_next;
    }
    
    html += '</select>'

    document.getElementById("month_select_cumul").innerHTML = html;
}



