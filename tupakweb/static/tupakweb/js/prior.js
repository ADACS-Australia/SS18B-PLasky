/**
 * Created by shibli on 25/08/18.
 */

$(document).ready(function () {


  var divs = []
  var $selected = $('#id_data-data_choice')
  var $data_simulated = $('#div_data_simulated')
  var $data_open = $('#div_data_open')
  if ($selected.val() === 'open') {
    divs.push($data_simulated)
  }

  if ($selected.val() === 'simulated') {
    divs.push($data_open)
  }

  hide_forms(divs)



  $selected.change(function () {
    divs = []
    divs.push($data_simulated)
    divs.push($data_open)
    hide_forms(divs)

    var detached_div = null

    if ($(this).val() === 'simulated') {
      detached_div = $('#form_store > #div_data_simulated').detach()
      detached_div.insertBefore('#data-tab-navigation')
    }

    if ($(this).val() === 'open') {
      detached_div = $('#form_store > #div_data_open').detach()
      detached_div.insertBefore('#data-tab-navigation')
    }
  })

  function hide_forms(divs) {
    $.each(divs, function () {
      var detached_div = $(this).detach()
      detached_div.appendTo('#form_store')
    })
  }
})
