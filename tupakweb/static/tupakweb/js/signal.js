/**
 * Created by shibli on 25/08/18.
 */

$(document).ready(function () {
  var divs = []
  var $selected = $('#id_signal-signal_choice')
  var $signal_parameter_bbh = $('#div_signal_parameter_bbh')
  var $same_model = $('.div-same_model')

  if ($selected.val() === 'skip') {
    divs.push($signal_parameter_bbh)
    divs.push($same_model)
  }

  if ($selected.val() === 'binary_black_hole') {
  }

  hide_forms(divs)

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
  })

  function hide_forms(divs) {
    $.each(divs, function () {
      var detached_div = $(this).detach()
      detached_div.appendTo('#form_store')
    })
  }
})
