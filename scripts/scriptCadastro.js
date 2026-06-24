const formCadastro = document.getElementById("formCadastro");

if (formCadastro) {

    formCadastro.addEventListener("submit", function (e) {

        e.preventDefault();

        const usuario = {
            nome: document.getElementById("cadastroNome").value,
            email: document.getElementById("cadastroEmail").value,
            senha: document.getElementById("cadastroSenha").value
        };

        localStorage.setItem(
            "usuario",
            JSON.stringify(usuario)
        );

        sessionStorage.setItem(
            "usuarioLogado",
            JSON.stringify(usuario)
        );

        alert("Cadastro realizado com sucesso!");

        window.location.href = "pacotes.html";
    });
}