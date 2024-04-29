/* Javascript for XBlockCompletionGrading. */
function XBlockCompletionGrading(runtime, element) {
    const calculateGrade = runtime.handlerUrl(element, "calculate_grade");
    console.log("XBlockCompletionGrading");
    $(element)
      .find("#calculate-grade")
      .click(function () {
        console.log("Calculating grade");
        const data = {};
        $.post(calculateGrade, JSON.stringify(data))
          .done(function (response) {
            if (response.success) {
              console.log(response);
              window.location.reload();
            } else {
              alert(response.message);
            }
          })
          .fail(function () {
            console.log("Error calculating grade");
          });
      });
  }
