boton = document.getElementById("btn-iniciar")

boton.addEventListener("click",validar)

function validar(){
    usuario = document.getElementById("usuario")
    if(usuario.value != ""){
        alert("Procesando datos");
    }else{
        alert("El campo no puede estar vacia")
    }
}