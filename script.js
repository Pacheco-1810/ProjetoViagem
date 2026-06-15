
let total = 0;

function adicionarPacote(nome, valor, idQuantidade) {

    const quantidade =
        parseInt(document.getElementById(idQuantidade).value);

    const subtotal = valor * quantidade;

    const lista = document.getElementById("listaCarrinho");

    const item = document.createElement("li");

    item.className =
        "list-group-item d-flex justify-content-between align-items-center";

    item.innerHTML = `
        <div>
            <strong>${nome}</strong><br>
            ${quantidade} viajante(s) - R$ ${subtotal.toLocaleString('pt-BR', {
                minimumFractionDigits: 2
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
        total.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
}
