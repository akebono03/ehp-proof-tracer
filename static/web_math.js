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
  }
);
