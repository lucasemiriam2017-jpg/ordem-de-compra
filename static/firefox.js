document.addEventListener("DOMContentLoaded", function () {
  console.log("firefox.js carregado");

  document.body.addEventListener("focus", function (e) {
    try {
      if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA")) {
        e.target.scrollIntoView({ block: "center", behavior: "smooth" });
      }
    } catch (err) {}
  }, true);

  var nums = document.querySelectorAll("input[type='number']");
  for (var i = 0; i < nums.length; i++) {
    (function(inp){
      inp.addEventListener("wheel", function(e){ e.preventDefault(); });
      inp.addEventListener("input", function(e){
        if(e.target.value && e.target.value.indexOf(",") !== -1){
          e.target.value = e.target.value.replace(",", ".");
        }
      });
    })(nums[i]);
  }

  var tbs = document.querySelectorAll("table");
  for (var j = 0; j < tbs.length; j++) {
    tbs[j].style.borderCollapse = "collapse";
  }

  if (typeof window.adicionarLinha !== "function") {
    console.warn("firefox.js: função adicionarLinha não encontrada.");
  }
  if (typeof window.gerarPDF !== "function") {
    console.warn("firefox.js: função gerarPDF não encontrada.");
  }
});
