// =========================
// CADASTRO
// =========================

const formCadastro = document.getElementById("formCadastro");

if (formCadastro) {

    formCadastro.addEventListener("submit", function(event) {

        event.preventDefault();

        const nome = document.getElementById("cadastroNome").value.trim();
        const email = document.getElementById("cadastroEmail").value.trim();
        const senha = document.getElementById("cadastroSenha").value.trim();

        let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];

        const emailExiste = usuarios.some(usuario => usuario.email === email);

        if (emailExiste) {
            alert("Este email já está cadastrado.");
            return;
        }

        const novoUsuario = {
            nome: nome,
            email: email,
            senha: senha
        };

        usuarios.push(novoUsuario);

        localStorage.setItem("usuarios", JSON.stringify(usuarios));

        alert("Cadastro realizado com sucesso!");

        formCadastro.reset();

        // Vai para a tela de login
        window.location.href = "Login.html";
    });

}


// =========================
// LOGIN
// =========================

const formLogin = document.getElementById("formLogin");

if (formLogin) {

    formLogin.addEventListener("submit", function(event) {

        event.preventDefault();

        const email = document.getElementById("loginEmail").value.trim();
        const senha = document.getElementById("loginSenha").value.trim();

        const usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];

        const usuarioEncontrado = usuarios.find(usuario =>
            usuario.email === email &&
            usuario.senha === senha
        );

        if (usuarioEncontrado) {

            localStorage.setItem(
                "usuarioLogado",
                JSON.stringify(usuarioEncontrado)
            );

            alert("Login realizado com sucesso!");

            // Troque para a página principal do projeto
            window.location.href = "index.html";

        } else {

            alert("Email ou senha incorretos.");

        }

    });

}