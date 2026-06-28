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

function finalizarCompra() {
    const usuario = JSON.parse(sessionStorage.getItem("usuarioLogado"));

    if (!usuario) {
        alert("Você precisa estar logado para finalizar a compra!");
        window.location.href = "Login.html";
        return;
    }

    if (total <= 0) {
        alert("Adicione pelo menos um pacote ao carrinho antes de finalizar.");
        return;
    }

    const historico = JSON.parse(
        localStorage.getItem("historicoViagens_" + usuario.email)
    ) || [];

    const descontoPercentual = calcularDescontoUsuario(usuario.email);

    const itensCarrinho = document.querySelectorAll("#listaCarrinho li");

    itensCarrinho.forEach(function (item) {
        const destino = item.querySelector("strong").textContent;

        const valorOriginal = total;

        const valorComDesconto = calcularValorComDesconto(
            valorOriginal,
            descontoPercentual
        );

        historico.push({
            destino: destino,
            valorOriginal: valorOriginal,
            desconto: descontoPercentual,
            valor: valorComDesconto,
            data: new Date().toLocaleDateString("pt-BR")
        });
    });

    localStorage.setItem(
        "historicoViagens_" + usuario.email,
        JSON.stringify(historico)
    );

    alert("Compra finalizada com sucesso! Desconto aplicado: " + descontoPercentual + "%");

    document.getElementById("listaCarrinho").innerHTML = "";
    total = 0;
    atualizarTotal();

    window.location.href = "Perfil.html";
}

function calcularDescontoUsuario(emailUsuario) {
    const historico = JSON.parse(
        localStorage.getItem("historicoViagens_" + emailUsuario)
    ) || [];

    const qtdViagens = historico.length;

    if (qtdViagens >= 10) {
        return 20;
    }

    if (qtdViagens >= 6) {
        return 15;
    }

    if (qtdViagens >= 3) {
        return 10;
    }

    return 5;
}
function calcularValorComDesconto(valor, descontoPercentual) {
    return valor - (valor * descontoPercentual / 100);
}
