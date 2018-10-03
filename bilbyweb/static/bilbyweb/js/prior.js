/**
 * Created by shibli on 25/08/18.
 */

$(document).ready(function () {

  function get_fixed_div_class(element_name) {
    return element_name.replace('_type', '_fixed').replace('prior-', 'div-')
  }

  function get_uniform_div_class(element_name) {
    return element_name.replace('_type', '_uniform').replace('prior-', 'div-')
  }

  $('.prior-type').each(function () {
    var divs = []

    var fixed_div_class = get_fixed_div_class($(this).attr('name'))
    var uniform_div_class = get_uniform_div_class($(this).attr('name'))
    console.log(fixed_div_class)
    console.log(uniform_div_class)

    var $fixed = $('.' + fixed_div_class)
    var $uniform = $('.' + uniform_div_class)

    if ($(this).val() === 'fixed') {
      divs.push($uniform)
    }

    if ($(this).val() === 'uniform') {
      divs.push($fixed)
    }

    hide_forms(divs)

    $(this).change(function () {
      console.log($(this).attr('name'))
      divs = []
      divs.push($fixed)
      divs.push($uniform)
      hide_forms(divs)

      var detached_div = null

      if ($(this).val() === 'fixed') {
        detached_div = $('#form_store >' + '.' + fixed_div_class).detach()
        $(this).parent().parent().after(detached_div)
      }

      if ($(this).val() === 'uniform') {
        detached_div = $('#form_store >' + '.' + uniform_div_class).detach()
        $(this).parent().parent().after(detached_div)
      }
    })

    function hide_forms(divs) {
      $.each(divs, function () {
        var detached_div = $(this).detach()
        detached_div.appendTo('#form_store')
      })
    }
  })
})
