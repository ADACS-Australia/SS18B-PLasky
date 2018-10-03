/**
 * Created by shibli on 25/08/18.
 */

$(document).ready(function () {
  var divs = []
  var $selected = $('#id_signal-signal_choice')
  var $signal_parameter_bbh = $('#div_signal_parameter_bbh')
  var $same_model = $('.div-same_model')
  var $signal_model = $('.div-signal_model')
  var $same_model_input = $('#id_signal-same_model')

  if ($selected.val() === 'skip') {
    divs.push($signal_parameter_bbh)
    divs.push($same_model)
  }

  if ($selected.val() === 'binary_black_hole') {
  }

  hide_forms(divs)
  show_hide_signal_model()

  $selected.change(function () {
    divs = []
    divs.push($signal_parameter_bbh)
    divs.push($same_model)
    hide_forms(divs)

    var detached_div = null

    if ($(this).val() === 'binary_black_hole') {
      detached_div = $('#form_store > #div_signal_parameter_bbh').detach()
      detached_div.appendTo('#signal-parameters')
      detached_div = $('#form_store > .div-same_model').detach()
      detached_div.appendTo('#signal-parameters')
    }
    show_hide_signal_model()
  })

  $same_model_input.change(function(){
    if ($(this).prop("checked")) {
			$(this).prop("checked", true);
		} else {
      $(this).prop("checked", false);
    }
    show_hide_signal_model()
  })

  function hide_forms(divs) {
    $.each(divs, function () {
      var detached_div = $(this).detach()
      detached_div.appendTo('#form_store')
    })
  }

  function show_hide_signal_model() {
    if ($same_model_input.prop('checked')) {
      if ($selected.val() === 'skip') {
        $signal_model.css('display', 'flex')
      } else {
        $signal_model.css('display', 'none')
      }
    } else {
      $signal_model.css('display', 'flex')
    }
  }
})
