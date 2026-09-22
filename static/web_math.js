document.addEventListener(
  "DOMContentLoaded",
  function () {
    const element = document.getElementById(
      "result-math"
    );

    if (
      element === null
      || typeof katex === "undefined"
    ) {
      return;
    }

    const latex = element.dataset.latex;

    if (!latex) {
      return;
    }

    katex.render(
      latex,
      element,
      {
        displayMode: true,
        throwOnError: false,
      }
    );
  }
);
