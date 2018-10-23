/**
 * Created by shibli on 27/09/18.
 */


$(document).ready(function () {
  $('.delete-job').on('click', function () {
    var job_name = $(this).parent().parent().find('.job-name > a').html()
    var link = $(this).attr('href')

    $(document).find('#deleteJob').find('.modal-body').find('p.job-name').html(job_name)
    $(document).find('#deleteJob').find('.modal-footer').find('a.delete').attr('href', link)
  })

  $('.cancel-job').on('click', function () {
    var job_name = $(this).parent().parent().find('.job-name > a').html()
    var link = $(this).attr('href')

    $(document).find('#cancelJob').find('.modal-body').find('p.job-name').html(job_name)
    $(document).find('#cancelJob').find('.modal-footer').find('a.cancel').attr('href', link)
  })
})
