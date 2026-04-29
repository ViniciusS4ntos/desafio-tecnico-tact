async function carregarDados() {
try {
const response = await fetch("http://127.0.0.1:8000/api/censo/");

    if (!response.ok) {
        throw new Error("Erro ao buscar API");
    }

    const data = await response.json();

    const total = document.getElementById("total");
    const max = document.getElementById("max");
    const tbody = document.getElementById("tabela-body");

    total.textContent = data.total_registros;

    let maiorBrasil = 0;

    data.dados.forEach((item) => {
        if (item.brasil > maiorBrasil) {
            maiorBrasil = item.brasil;
        }

        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${item.grupo_idade}</td>
            <td>${item.brasil.toLocaleString("pt-BR")}</td>
            <td>${item.norte.toLocaleString("pt-BR")}</td>
            <td>${item.nordeste.toLocaleString("pt-BR")}</td>
            <td>${item.sudeste.toLocaleString("pt-BR")}</td>
            <td>${item.sul.toLocaleString("pt-BR")}</td>
            <td>${item.centro_oeste.toLocaleString("pt-BR")}</td>
        `;

        tbody.appendChild(tr);
    });

    max.textContent = maiorBrasil.toLocaleString("pt-BR");
    console.log(data.dados);
} catch (erro) {
    console.error("Erro:", erro);
}

}

carregarDados();