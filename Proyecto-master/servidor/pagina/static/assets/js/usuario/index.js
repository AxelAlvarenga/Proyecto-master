function listaproductos(){
    $.ajax({
        url:"/pagina/cargar_compra",
        type:"get",
        dataType:"json",
        success:function(response){
            console.log(response);
        },
        error:function(error){
            console.log(error); 
        }
    });

}

$(document).ready(function(){
    listaproductos();

})