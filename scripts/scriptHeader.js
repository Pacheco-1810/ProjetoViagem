document.addEventListener("DOMContentLoaded", () => {

    const areaUsuario = document.getElementById("areaUsuario");

    if (!areaUsuario) return;

    const usuario =
        JSON.parse(sessionStorage.getItem("usuarioLogado"));

    if (usuario) {

        areaUsuario.innerHTML = `
            <span class="text-white fw-bold fs-5">
                Oi, ${usuario.nome}
            </span>

            <button
                class="btn btn-danger"
                onclick="logout()">
                Sair
            </button>
        `;
    }
});

function logout() {

    sessionStorage.removeItem("usuarioLogado");

    window.location.reload();
}