function menu(){
    var arr = location.pathname.split("/")
    switch (arr[1]){
        case "":
            $("#mnu_home").addClass("active")
            $("#a_home").addClass("active")
            break;
        case "reservaciones":
            $("#mnu_reservas").addClass("active")
            //$("#a_reservas").addClass("active")
            break;
        case "informes":
            $("#mnu_informes").addClass("active")
            //$("#a_informes").addClass("active")
            break;
        case "reportes":
            $("#mnu_reportes").addClass("active")
            //$("#a_reportes").addClass("active")
            break;
        case "administracion":
            $("#mnu_admon").addClass("active")
            //$("#a_reportes").addClass("active")
            break;
        default:
            break;


    }
}

$( document ).ready( function() {
menu();
});
