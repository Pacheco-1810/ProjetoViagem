const formLogin = document.getElementById("formLogin");

if (formLogin) {

    formLogin.addEventListener("submit", function (e) {

        e.preventDefault();

        const email =
            document.getElementById("loginEmail").value;

        const senha =
            document.getElementById("loginSenha").value;

        const usuario =
            JSON.parse(localStorage.getItem("usuario"));

        if (
            usuario &&
            usuario.email === email &&
            usuario.senha === senha
        ) {

            sessionStorage.setItem(
                "usuarioLogado",
                JSON.stringify(usuario)
            );

            alert("Login realizado com sucesso!");

            window.location.href = "pacotes.html";

        } else {

            alert("E-mail ou senha inválidos.");
        }
    });
}