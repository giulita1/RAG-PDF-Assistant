let archivoSeleccionado = null;
let pdfCargado = false;

const pdfInput = document.getElementById("pdf_input");
const inputPregunta = document.getElementById("input_chatear");
const btnEnviar = document.getElementById("btn_enviar");
const btnReset = document.getElementById("btn_reset");

pdfInput.addEventListener("change", function () {

     if(pdfCargado){
        alert("A PDF is already active. Reset to upload a new one");
        pdfInput.value = "";
        return;
    }
    
    const archivo = pdfInput.files[0];
    if(!archivo) return;

    if(archivo.type !== 'application/pdf'){
        alert("Please upload a PDF file.");
        pdfInput.value = "";
        archivo = null;
        return;
    }

    if(file.size > 10 * 1024 * 1024){
        alert("File is too large: max 10MB");
        pdfInput.value = "";
        archivo = null;
        return;
    }

   
    archivoSeleccionado = archivo; 

});

btnEnviar.addEventListener("click", enviarMensaje);

inputPregunta.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        enviarMensaje();
    }
});

async function enviarMensaje() {

    if(!archivoSeleccionado && !pdfCargado){
        alert("Upload a PDF");
        return;
    }

    const pregunta = inputPregunta.value.trim();
    if (!pregunta) return;

    agregarMensaje(pregunta, "user");
    inputPregunta.value = "";

    const formData = new FormData();

    formData.append("pregunta", pregunta);

    if (archivoSeleccionado) {
        formData.append("file", archivoSeleccionado);
    
    }
    const mensajeCargando = agregarMensaje("Thinking...","bot");

    try{
    const response = await fetch("https://rag-pdf-assistant-xeic.onrender.com/chat", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if(!response.ok){
        mensajeCargando.textContent = data.error || data.answer;
        return;
    }

    if(archivoSeleccionado){
        pdfCargado = true;
        archivoSeleccionado = null;
        pdfInput.value = "";
    }

    if(data.error){
        mensajeCargando.textContent=data.error;
        return;
    }

    mensajeCargando.textContent = data.answer;
}catch(error){
    mensajeCargando.textContent = "Could not connect to the server";
}
}

btnReset.addEventListener("click", async () => {

    await fetch("https://rag-pdf-assistant-xeic.onrender.com/reset", { method: "POST" });
    pdfCargado = false;
    archivoSeleccionado = null;

    document.getElementById("mensajes").innerHTML = "";
    document.getElementById("pdf_input").value = "";
    document.getElementById("input_chatear").value = "";
});

function agregarMensaje(texto, tipo){

    const contenedor = document.getElementById("mensajes");
    const mensaje = document.createElement("div");
    mensaje.classList.add("mensaje");

    if(tipo=="user"){

        mensaje.classList.add("user");

    }else if (tipo=="bot"){
        mensaje.classList.add("bot");
    }

    mensaje.textContent = texto;
    contenedor.appendChild(mensaje);

    contenedor.scrollTop = contenedor.scrollHeight;

    return mensaje;

}