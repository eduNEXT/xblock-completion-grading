/* Javascript for XBlockCompletionGrading. */
function XBlockCompletionGrading(runtime, element) {
    const calculateGrade = runtime.handlerUrl(element, "calculate_grade");

    let gettext;
    if ("CompletionGradingI18n" in window || "gettext" in window) {
      gettext = window.CompletionGradingI18n?.gettext || window.gettext;
    }

    if (typeof gettext == "undefined") {
      // No translations -- used by test environment
      gettext = (string) => string;
    }

    $(element)
      .find("#calculate-grade")
      .click(function () {
        const data = {};
        $.post(calculateGrade, JSON.stringify(data))
          .done(function (response) {
            if (response.success) {
              window.location.reload();
            } else {
              $(element).find("#error-message").text(gettext(response.message));
            }
          })
          .fail(function () {
            console.log("Error calculating grade");
          });
      });
  }
