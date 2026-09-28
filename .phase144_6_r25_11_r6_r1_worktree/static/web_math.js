document.addEventListener(
  "DOMContentLoaded",
  function () {
    if (
      typeof katex === "undefined"
    ) {
      return;
    }

    const elements = (
      document.querySelectorAll(
        "[data-latex]"
      )
    );

    elements.forEach(
      function (element) {
        const latex = (
          element.dataset.latex
        );

        if (!latex) {
          return;
        }

        const displayMode = (
          !element.classList.contains(
            "group-proof-rendered-inline-math"
          )
        );

        katex.render(
          latex,
          element,
          {
            displayMode: displayMode,
            throwOnError: false,
          }
        );
      }
    );
  }
);
