// firefox.js — correções específicas para Firefox
document.addEventListener("DOMContentLoaded", function () {
  console.log("firefox.js carregado");

  // evita comportamento de scroll estranho ao focar inputs
  document.body.addEventListener("focus", function (e) {
    try {
      if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA")) {
        e.target.scrollIntoView({ block: "center", behavior: "smooth" });
      }
    } catch (err) { /* silencioso */ }
  }, true);

  // garante que botões com onclick inline chamem as funções globais
  // (index.html já expõe window.adicionarLinha / gerarPDF / limpar)
  // não é necessário re-declarar — isto apenas avisa caso falte.
  if (typeof window.adicionarLinha !== "function") {
    console.warn("firefox.js: função adicionarLinha não encontrada.");
  }
  if (typeof window.gerarPDF !== "function") {
    console.warn("firefox.js: função gerarPDF não encontrada.");
  }

  // pequenas proteções para inputs number no Firefox
  var nums = document.querySelectorAll("input[type='number']");
  for (var i = 0; i < nums.length; i++) {
    (function(inp){
      inp.addEventListener("wheel", function(e){ e.preventDefault(); });
      inp.addEventListener("input", function(e){
        if (e.target.value && e.target.value.indexOf(",") !== -1) {
          e.target.value = e.target.value.replace(",", ".");
        }
      });
    })(nums[i]);
  }

  // força collapse de bordas para tabelas (corrige visual)
  var tbs = document.querySelectorAll("table");
  for (var j = 0; j < tbs.length; j++) {
    tbs[j].style.borderCollapse = "collapse";
  }
});
