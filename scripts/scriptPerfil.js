document.addEventListener("DOMContentLoaded", function () {
    carregarPerfil();
});

function carregarPerfil() {
    const usuarioLogado = JSON.parse(sessionStorage.getItem("usuarioLogado"));

    const avisoLogin = document.getElementById("avisoLogin");
    const areaPerfil = document.getElementById("areaPerfil");

    if (!usuarioLogado) {
        avisoLogin.classList.remove("d-none");
        areaPerfil.classList.add("d-none");
        return;
    }

    avisoLogin.classList.add("d-none");
    areaPerfil.classList.remove("d-none");

    document.getElementById("perfilNome").textContent = usuarioLogado.nome || "Usuário";
    document.getElementById("perfilEmail").textContent = usuarioLogado.email || "E-mail não informado";

    atualizarDashboard(usuarioLogado.email);
}

function atualizarDashboard(emailUsuario) {
    const historico = buscarHistorico(emailUsuario);

    const qtdViagens = historico.length;
    const totalGasto = historico.reduce((total, viagem) => total + viagem.valor, 0);

    const dadosNivel = calcularNivel(qtdViagens);

    document.getElementById("qtdViagens").textContent = qtdViagens;
    document.getElementById("totalGasto").textContent = formatarMoeda(totalGasto);
    document.getElementById("nivelUsuario").textContent = dadosNivel.nivel;
    document.getElementById("descontoUsuario").textContent = dadosNivel.desconto + "% de desconto";
    document.getElementById("proximoNivel").textContent = dadosNivel.proximoNivel;
    document.getElementById("barraNivel").style.width = dadosNivel.progresso + "%";
    document.getElementById("barraNivel").textContent = dadosNivel.progresso + "%";
    document.getElementById("textoProgresso").textContent = dadosNivel.texto;

    renderizarHistorico(historico);
}

function calcularNivel(qtdViagens) {
    if (qtdViagens >= 10) {
        return {
            nivel: "Diamante",
            desconto: 20,
            proximoNivel: "Máximo",
            progresso: 100,
            texto: "Parabéns! Você chegou ao nível máximo e desbloqueou 20% de desconto."
        };
    }

    if (qtdViagens >= 6) {
        return {
            nivel: "Ouro",
            desconto: 15,
            proximoNivel: "Diamante",
            progresso: calcularProgresso(qtdViagens, 6, 10),
            texto: `Faltam ${10 - qtdViagens} viagem(ns) para chegar ao nível Diamante.`
        };
    }

    if (qtdViagens >= 3) {
        return {
            nivel: "Prata",
            desconto: 10,
            proximoNivel: "Ouro",
            progresso: calcularProgresso(qtdViagens, 3, 6),
            texto: `Faltam ${6 - qtdViagens} viagem(ns) para chegar ao nível Ouro.`
        };
    }

    return {
        nivel: "Bronze",
        desconto: 5,
        proximoNivel: "Prata",
        progresso: calcularProgresso(qtdViagens, 0, 3),
        texto: `Faltam ${3 - qtdViagens} viagem(ns) para chegar ao nível Prata.`
    };
}

function calcularProgresso(valorAtual, minimo, maximo) {
    const progresso = ((valorAtual - minimo) / (maximo - minimo)) * 100;
    return Math.min(Math.max(Math.round(progresso), 0), 100);
}

function buscarHistorico(emailUsuario) {
    const chave = "historicoViagens_" + emailUsuario;
    return JSON.parse(localStorage.getItem(chave)) || [];
}

function salvarHistorico(emailUsuario, historico) {
    const chave = "historicoViagens_" + emailUsuario;
    localStorage.setItem(chave, JSON.stringify(historico));
}

function renderizarHistorico(historico) {
    const area = document.getElementById("historicoViagens");

    if (historico.length === 0) {
        area.innerHTML = `
            <div class="alert alert-info">
                Você ainda não possui viagens compradas.
            </div>
        `;
        return;
    }

    area.innerHTML = "";

    historico.forEach((viagem, index) => {
        const item = document.createElement("article");
        item.className = "card mb-3 shadow-sm animar-card";

        item.innerHTML = `
            <div class="card-body d-flex justify-content-between align-items-center">
                <div>
                    <h5>${viagem.destino}</h5>
                    <p class="mb-1">Data: ${viagem.data}</p>
                    <p class="mb-0">Valor: R$ ${formatarMoeda(viagem.valor)}</p>
                </div>

                <span class="badge text-bg-success">Compra ${index + 1}</span>
            </div>
        `;

        area.appendChild(item);
    });
}


function formatarMoeda(valor) {
    return valor.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}