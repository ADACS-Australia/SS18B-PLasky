JOB_COMPLETION = dict()
JOB_COMPLETION['subject'] = '[BILBY-WEB] Job Finished with {}'
JOB_COMPLETION['message'] = '<p>Dear {{first_name}} {{last_name}}</p>' \
                            '<p>The job you launched has been finished processing.</p>' \
                            '<p>The status of the job is: {{job_status}}.</p>' \
                            '<p> You can view the job and the output by clicking on the following ' \
                            '<a href="{{link}}" target="_blank">link</a>:</p>' \
                            '<p><a href="{{link}}" target="_blank">{{link}}</a></p>' \
                            '<p>Thank you very much for using Bilby.</p>' \
                            '<p>&nbsp;</p>' \
                            '<p>Regards,</p>' \
                            '<p>BILBY Team</p>'
