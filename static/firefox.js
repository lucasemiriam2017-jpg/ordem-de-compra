document.addEventListener("DOMContentLoaded", function() {
  let contador = 1;
  const tabelaBody = document.querySelector("#tabela_itens tbody");
  let itens = [];

  // Função para criar e adicionar uma linha de produto
  window.adicionarLinha = function() {
    if (!tabelaBody) {
      console.error("Tabela de produtos não encontrada!");
      return;
    }

    const tr = document.createElement("tr");

    // Item
    const tdItem = document.createElement("td");
    tdItem.className = "text-center";
    tdItem.textContent = contador;

    // Quantidade
    const tdQtd = document.createElement("td");
    const inpQtd = document.createElement("input");
    inpQtd.type = "number";
    inpQtd.min = 0;
    inpQtd.className = "form-control qtd";
    tdQtd.appendChild(inpQtd);

    // Código
    const tdCod = document.createElement("td");
    const inpCod = document.createElement("input");
    inpCod.type = "text";
    inpCod.className = "form-control cod";
    tdCod.appendChild(inpCod);

    // Descrição
    const tdDesc = document.createElement("td");
    const inpDesc = document.createElement("input");
    inpDesc.type = "text";
    inpDesc.className = "form-control desc";
    tdDesc.appendChild(inpDesc);

    // Preço Unitário
    const tdPreco = document.createElement("td");
    const inpPreco = document.createElement("input");
    inpPreco.type = "text";
    inpPreco.className = "form-control preco";
    inpPreco.value = "0,00";
    tdPreco.appendChild(inpPreco);

    // Total
    const tdTotal = document.createElement("td");
    tdTotal.className = "text-end total";
    tdTotal.textContent = "0,00";

    // Ações (remover)
    const tdAcoes = document.createElement("td");
    tdAcoes.className = "text-center";
    const btnRem = document.createElement("button");
    btnRem.type = "button";
    btnRem.className = "btn btn-sm btn-danger btn-remover";
    btnRem.textContent = "X";
    btnRem.addEventListener("click", () => {
      tr.remove();
      calcularTotais();
    });
    tdAcoes.appendChild(btnRem);

    // Monta a linha
    tr.append(tdItem, tdQtd, tdCod, tdDesc, tdPreco, tdTotal, tdAcoes);
    tabelaBody.appendChild(tr);

    // Atualiza contador
    contador++;

    // Adiciona eventos de input para recalcular totais automaticamente
    [inpQtd, inpPreco].forEach(inp => {
      inp.addEventListener("input", calcularTotais);
      inp.addEventListener("wheel", e => e.preventDefault()); // previne scroll no Firefox
    });
  };

  // Função para recalcular totais
  function calcularTotais() {
    itens = [];
    tabelaBody.querySelectorAll("tr").forEach(tr => {
      const qtd = parseFloat(tr.querySelector(".qtd")?.value.replace(",", ".") || 0);
      const preco = parseFloat(tr.querySelector(".preco")?.value.replace(/\./g, "").replace(",", ".") || 0);
      const total = qtd * preco;
      tr.querySelector(".total").textContent = total.toLocaleString("pt-BR", { minimumFractionDigits: 2 });
      itens.push({
        qtd: qtd.toString(),
        cod: tr.querySelector(".cod")?.value || "",
        desc: tr.querySelector(".desc")?.value || "",
        preco: preco.toLocaleString("pt-BR", { minimumFractionDigits: 2 }),
        tot: total.toLocaleString("pt-BR", { minimumFractionDigits: 2 })
      });
    });
  }

  // Conecta o botão ao evento
  const btnAdd = document.getElementById("btnAdicionarProduto");
  if (btnAdd) btnAdd.addEventListener("click", window.adicionarLinha);
});
