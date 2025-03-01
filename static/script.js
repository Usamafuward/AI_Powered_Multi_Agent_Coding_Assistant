// Add HTMX interactions or other JavaScript logic here
document
  .getElementById("generate-code-btn")
  .addEventListener("click", async () => {
    const prompt = document.getElementById("code-prompt").value;
    const response = await fetch(
      `/generate_code?prompt=${encodeURIComponent(prompt)}`
    );
    const data = await response.json();
    document.getElementById("generated-code").textContent = data.code;
  });

document
  .getElementById("debug-code-btn")
  .addEventListener("click", async () => {
    const code = document.getElementById("debug-code-input").value;
    const response = await fetch(
      `/debug_code?code=${encodeURIComponent(code)}`
    );
    const data = await response.json();
    document.getElementById("debugged-code").textContent = data.debugged_code;
  });

document
  .getElementById("optimize-code-btn")
  .addEventListener("click", async () => {
    const code = document.getElementById("optimize-code-input").value;
    const response = await fetch(
      `/optimize_code?code=${encodeURIComponent(code)}`
    );
    const data = await response.json();
    document.getElementById("optimized-code").textContent = data.optimized_code;
  });
