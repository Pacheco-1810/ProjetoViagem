document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("formContato");
    const mensagemContato = document.getElementById("mensagemContato");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        if (!form.checkValidity()) {
            form.classList.add("was-validated");
            return;
        }

        mensagemContato.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                Mensagem enviada com sucesso! Em breve entraremos em contato.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        form.reset();
        form.classList.remove("was-validated");
    });
});