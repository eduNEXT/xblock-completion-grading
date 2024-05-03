
            (function(global){
                var CompletionGradingI18n = {
                  init: function() {
                    

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "Button Text": "Texto del Bot\u00f3n",
    "Calculate Grade": "Calcular Calificaci\u00f3n",
    "Completion grade calculation failed. Try again later.": "Error en el c\u00e1lculo de la calificaci\u00f3n de finalizaci\u00f3n. Vuelva a intentarlo m\u00e1s tarde.",
    "Completion grading method for the component. There are two options: minimum completion and weighted completion. Minimum completion grades learners based on the minimum number of completed units, if the learner has completed the minimum number of units, they will get a grade of 1, otherwise 0. Weighted completion grades learners based on the weighted number of completed units, if the learner has completed a number of units greater or equal to the number of completed units required to get a grade, they will get a grade of 1, otherwise the grade will be the number of completed units divided by the number of completed units required to get a grade configured in the component.If the value is not set, the component will use the minimum completion method.The unit completions don't include the completion of the unit that contains the component.": "M\u00e9todo de calificaci\u00f3n para el componente. Hay dos opciones: finalizaci\u00f3n m\u00ednima y finalizaci\u00f3n media. La finalizaci\u00f3n m\u00ednima califica a los estudiantes en funci\u00f3n al n\u00famero m\u00ednimo de unidades completadas, si el alumno ha completado el n\u00famero m\u00ednimo de unidades, obtendr\u00e1 una calificaci\u00f3n de 1; en caso contrario, 0. La finalizaci\u00f3n media califica a los estudiantes en funci\u00f3n del n\u00famero medio de unidades completadas; si el alumno ha completado un n\u00famero de unidades superior o igual al n\u00famero de unidades completadas necesario para obtener una calificaci\u00f3n, obtendr\u00e1 una calificaci\u00f3n de 1; en caso contrario, la calificaci\u00f3n ser\u00e1 el n\u00famero de unidades completadas dividido por el n\u00famero de unidades completadas necesario para obtener una calificaci\u00f3n configurado en el componente. Si el valor no est\u00e1 configurado, el componente utilizar\u00e1 el m\u00e9todo de finalizaci\u00f3n m\u00ednima. Las unidades completadas no incluyen la finalizaci\u00f3n de la unidad que contiene el componente.",
    "Course Completion Grading": "Calificaci\u00f3n por Nivel de Finalizaci\u00f3n del Curso",
    "Defines the number of points this problem is worth. If the value is not set, the problem is worth 10 points.": "Define el n\u00famero de puntos que vale este problema. Si el valor no est\u00e1 establecido, el problema vale 10 puntos.",
    "Defines the number of times a student can attempt to calculate the grade. If the value is not set, infinite attempts are allowed.": "Define el n\u00famero de veces que un estudiante puede intentar calcular la calificaci\u00f3n. Si el valor no est\u00e1 establecido, se permiten intentos indefinidos.",
    "Display Name": "Nombre a Mostrar",
    "Grade calculations for your latest completion state are in progress. Try again in a few seconds.": "Los c\u00e1lculos de calificaciones para tu \u00faltimo estado de finalizaci\u00f3n est\u00e1n en progreso. Int\u00e9ntalo de nuevo en unos segundos.",
    "Grading Method": "M\u00e9todo de Calificaci\u00f3n",
    "Instructions Text": "Texto de las Instrucciones",
    "Instructions to be displayed to the student.": "Define el texto de las instrucciones que se mostrar\u00e1 al estudiante.",
    "Maximum Attempts": "N\u00famero M\u00e1ximo de Intentos",
    "Minimum Number of Completed Units": "N\u00famero M\u00ednimo de Unidades Completadas",
    "Number of Completed Units": "N\u00famero de Unidades Completadas",
    "Number of attempts taken by the student to calculate the grade.": "N\u00famero de intentos tomados por el estudiante para calcular la calificaci\u00f3n.",
    "Number of units that need to be completed to get a grade.": "N\u00famero de unidades que deben completarse para obtener una calificaci\u00f3n.",
    "Please press the button to calculate your grade according to the number of completed units in the course.": "Por favor, presiona el bot\u00f3n para calcular su nota seg\u00fan el n\u00famero de unidades completadas en el curso.",
    "Problem Weight": "Peso del Problema",
    "Raw score": "Puntuaci\u00f3n Bruta",
    "Submission UUID": "UUID de la Entrega",
    "Task ID": "ID de la tarea as\u00edncrona",
    "Text to be displayed on the button.": "Define el texto que se mostrar\u00e1 en el bot\u00f3n.",
    "The display name for this component.": "El nombre para mostrar de este componente.",
    "The raw score for the assignment.": "La puntuaci\u00f3n bruta para la tarea.",
    "The submission UUID for the assignment.": "El UUID de la entrega para la tarea.",
    "The task ID for the unit completions calculation task.": "El ID de tarea para la tarea de c\u00e1lculo de unidades completadas.",
    "Weighted Number of Completed Units": "N\u00famero Ponderado de Unidades Terminadas",
    "You have made": "Has hecho",
    "You have reached the maximum number of attempts.": "Has alcanzado el n\u00famero m\u00e1ximo de intentos.",
    "Your score is:": "Tu puntuaci\u00f3n es:",
    "attempts to calculate the grading.": "intentos para calcular la calificaci\u00f3n."
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%y %H:%M:%S",
      "%d/%m/%y %H:%M:%S.%f",
      "%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
    "SHORT_DATE_FORMAT": "d/m/Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};


                  }
                };
                CompletionGradingI18n.init();
                global.CompletionGradingI18n = CompletionGradingI18n;
            }(this));
        