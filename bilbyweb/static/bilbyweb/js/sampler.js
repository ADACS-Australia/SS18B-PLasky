/**
 * Created by shibli on 5/09/18.
 */

$(document).ready(function () {
  var divs = []
  var $selected = $('#id_sampler-sampler_choice')
  var $sampler_dynesty = $('#div_sampler_dynesty')
  var $sampler_nestle = $('#div_sampler_nestle')
  var $sampler_emcee = $('#div_sampler_emcee')

  if ($selected.val() === 'dynesty') {
    divs.push($sampler_nestle)
    divs.push($sampler_emcee)
  } else if ($selected.val() === 'nestle') {
    divs.push($sampler_dynesty)
    divs.push($sampler_emcee)
  } else if ($selected.val() === 'emcee') {
    divs.push($sampler_dynesty)
    divs.push($sampler_nestle)
  }

  hide_forms(divs)

  $selected.change(function () {
    divs = []
    divs.push($sampler_dynesty)
    divs.push($sampler_nestle)
    divs.push($sampler_emcee)
    hide_forms(divs)

    var detached_div = null

    if ($(this).val() === 'dynesty') {
      detached_div = $('#form_store > #div_sampler_dynesty').detach()
      detached_div.insertBefore('#sampler-tab-navigation')
    } else if ($(this).val() === 'nestle') {
      detached_div = $('#form_store > #div_sampler_nestle').detach()
      detached_div.insertBefore('#sampler-tab-navigation')
    } else if ($(this).val() === 'emcee') {
      detached_div = $('#form_store > #div_sampler_emcee').detach()
      detached_div.insertBefore('#sampler-tab-navigation')
    }

  })

  function hide_forms(divs) {
    $.each(divs, function () {
      var detached_div = $(this).detach()
      detached_div.appendTo('#form_store')
    })
  }
})
