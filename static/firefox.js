// 🔥 Ajustes especiais para Firefox
document.addEventListener("DOMContentLoaded", () => {
  console.log("🔥 Correções para Firefox aplicadas");

  // Força foco nos inputs criados dinamicamente (Firefox não aplicava automaticamente)
  document.body.addEventListener("focus", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") {
      e.target.scrollIntoView({ block: "center", behavior: "smooth" });
    }
  }, true);

  // Garante que o botão "Adicionar Produto" funcione corretamente
  const addButton = document.getElementById("adicionarProduto");
  if (addButton) {
    addButton.addEventListener("click", (e) => {
      e.preventDefault();
      if (typeof adicionarLinha === "function") {
        adicionarLinha();
      } else {
        console.warn("⚠️ Função adicionarLinha não encontrada");
      }
    });
  }

  // Corrige comportamento do botão de gerar PDF
  const btnGerar = document.getElementById("btnGerarPdf");
  if (btnGerar) {
    btnGerar.addEventListener("click", (e) => {
      e.preventDefault();

      try {
        if (typeof gerarPDF === "function") {
          gerarPDF();
        } else {
          console.warn("⚠️ Função gerarPDF não encontrada");
        }
      } catch (err) {
        console.error("❌ Erro ao tentar gerar o PDF no Firefox:", err);
        alert("Erro ao gerar PDF. Tente novamente.");
      }
    });
  }

  // Corrige formatação dos inputs numéricos no Firefox
  document.querySelectorAll("input[type='number']").forEach(input => {
    input.addEventListener("wheel", (e) => e.preventDefault());
    input.addEventListener("input", (e) => {
      if (e.target.value.includes(",")) {
        e.target.value = e.target.value.replace(",", ".");
      }
    });
  });

  // Ajuste visual fino (Firefox tinha margens extras em tabelas dinâmicas)
  const tabelas = document.querySelectorAll("table");
  tabelas.forEach(tb => {
    tb.style.borderCollapse = "collapse";
  });
});
