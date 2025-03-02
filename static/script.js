document.addEventListener("DOMContentLoaded", () => {
  const BASE_URL = "http://localhost:8011/api"; // Update with your backend URL

  // Code Generator
  document
    .getElementById("generate-code-btn")
    .addEventListener("click", async () => {
      const prompt = document.getElementById("code-prompt").value;

      if (!prompt.trim()) {
        alert("Please enter a prompt.");
        return;
      }

      try {
        const response = await fetch(`${BASE_URL}/generate-code`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prompt,
            language: "python",
            debug: true,
            optimize: true,
            document: true,
          }),
        });

        const data = await response.json();
        const task_id = data.task_id;

        // Poll for task completion
        const interval = setInterval(async () => {
          const statusResponse = await fetch(`${BASE_URL}/task/${task_id}`);
          const statusData = await statusResponse.json();

          if (statusData.status === "completed") {
            clearInterval(interval);
            document.getElementById("generated-code").textContent =
              statusData.result.code;
          } else if (statusData.status === "failed") {
            clearInterval(interval);
            alert(`Task failed: ${statusData.result.error}`);
          }
        }, 2000);
      } catch (error) {
        console.error("Error generating code:", error);
        alert("An error occurred while generating code.");
      }
    });

  // Debugger
  document
    .getElementById("debug-code-btn")
    .addEventListener("click", async () => {
      const code = document.getElementById("debug-code-input").value;

      if (!code.trim()) {
        alert("Please enter code to debug.");
        return;
      }

      try {
        const response = await fetch(`${BASE_URL}/debug-code`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, language: "python" }),
        });

        const data = await response.json();
        const task_id = data.task_id;

        // Poll for task completion
        const interval = setInterval(async () => {
          const statusResponse = await fetch(`${BASE_URL}/task/${task_id}`);
          const statusData = await statusResponse.json();

          if (statusData.status === "completed") {
            clearInterval(interval);
            document.getElementById("debugged-code").textContent =
              statusData.result.code;
          } else if (statusData.status === "failed") {
            clearInterval(interval);
            alert(`Task failed: ${statusData.result.error}`);
          }
        }, 2000);
      } catch (error) {
        console.error("Error debugging code:", error);
        alert("An error occurred while debugging code.");
      }
    });

  // Optimizer
  document
    .getElementById("optimize-code-btn")
    .addEventListener("click", async () => {
      const code = document.getElementById("optimize-code-input").value;

      if (!code.trim()) {
        alert("Please enter code to optimize.");
        return;
      }

      try {
        const response = await fetch(`${BASE_URL}/optimize-code`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            code,
            language: "python",
            optimization_target: "performance",
          }),
        });

        const data = await response.json();
        const task_id = data.task_id;

        // Poll for task completion
        const interval = setInterval(async () => {
          const statusResponse = await fetch(`${BASE_URL}/task/${task_id}`);
          const statusData = await statusResponse.json();

          if (statusData.status === "completed") {
            clearInterval(interval);
            document.getElementById("optimized-code").textContent =
              statusData.result.code;
          } else if (statusData.status === "failed") {
            clearInterval(interval);
            alert(`Task failed: ${statusData.result.error}`);
          }
        }, 2000);
      } catch (error) {
        console.error("Error optimizing code:", error);
        alert("An error occurred while optimizing code.");
      }
    });
});
