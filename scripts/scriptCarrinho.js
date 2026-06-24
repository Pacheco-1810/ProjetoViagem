let total = 0;

window.onload = function () {

    const pacotePendente =
        JSON.parse(sessionStorage.getItem("pacotePendente"));

    const usuario =
        JSON.parse(sessionStorage.getItem("usuarioLogado"));

    if (pacotePendente && usuario) {

        adicionarPacoteAoCarrinho(
            pacotePendente.nome,
            pacotePendente.valor,
            pacotePendente.quantidade
        );

        sessionStorage.removeItem("pacotePendente");
    }
};

function adicionarPacote(nome, valor, idQuantidade) {

    const usuario =
        JSON.parse(sessionStorage.getItem("usuarioLogado"));

    const quantidade =
        parseInt(document.getElementById(idQuantidade).value);

    if (!usuario) {

        sessionStorage.setItem(
            "pacotePendente",
            JSON.stringify({
                nome,
                valor,
                quantidade
            })
        );

        alert("Você precisa realizar login para adicionar itens ao carrinho.");

        window.location.href = "Login.html";

        return;
    }

    adicionarPacoteAoCarrinho(
        nome,
        valor,
        quantidade
    );
}

function adicionarPacoteAoCarrinho(nome, valor, quantidade) {

    const subtotal = valor * quantidade;

    const lista =
        document.getElementById("listaCarrinho");

    const item =
        document.createElement("li");

    item.className =
        "list-group-item d-flex justify-content-between align-items-center";

    item.innerHTML = `
        <div>
            <strong>${nome}</strong><br>
            ${quantidade} viajante(s) - R$ ${subtotal.toLocaleString('pt-BR', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })}
        </div>

        <button
            class="btn btn-sm btn-danger"
            onclick="removerItem(this, ${subtotal})">
            ✖
        </button>
    `;

    lista.appendChild(item);

    total += subtotal;

    atualizarTotal();
}

function removerItem(botao, valor) {

    botao.parentElement.remove();

    total -= valor;

    atualizarTotal();
}

function atualizarTotal() {

    document.getElementById("totalCarrinho").textContent =
        total.toLocaleString("pt-BR", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
}