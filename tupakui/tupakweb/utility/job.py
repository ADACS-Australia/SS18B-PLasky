from ..models import (
    Job,
    Data, DataOpen, DataSimulated,
    Signal, SignalBbhParameter,
    Prior, PriorFixed, PriorUniform,
    Sampler, SamplerDynesty, SamplerEmcee, SamplerNestle,
)

def get_signal_options(job_id, response=None):
    """Returns the next set of questions

    Parameters
    ----------
    job_id:
        Id of the job
    response:
        response object of the database model

    Returns
    -------
    signal_objects:
        list of job objects
    """
    job = Job.objects.get(id=job_id)

    signal_choice = Signal.objects.filter(job=job)

    signal_objects = []

    for job_question in job_questions:
        visited = False
        galaxy = job_question.job_element.galaxy

        # get question choices
        options = QuestionOption.objects.filter(question=job_question.job_element.question)

        choices = []
        default_choice = None
        for option in options:
            choices.append((option.option, option.option))
            if option.is_default_option:
                default_choice = option.option

        # overriding the default with provided answers if any
        try:
            default_choice = QuestionResponse.objects.get(
                response=response,
                job_question=job_question,
            ).answer
            visited = True
        except QuestionResponse.DoesNotExist:
            pass

        q = Sq(
            name=constants.FORM_QUESTION_PREFIX + job_question.id.__str__(),
            label=job_question.job_element.question.text,
            choices=tuple(choices),
            initial=default_choice,
            question_type=job_question.job_element.question.category,
        )

        # getting images for this job question
        image_stores = ImageStore.objects.filter(galaxy=galaxy)
        divs = []
        scripts = []
        for index, image_store in enumerate(image_stores):
            try:
                question_drawn_response = QuestionDrawnResponse.objects.get(
                    response=response,
                    job_question=job_question,
                    image=image_store,
                )
                x_coordinates = question_drawn_response.x_coordinates
                y_coordinates = question_drawn_response.y_coordinates
                pre_filled = dict(
                    x=x_coordinates.split(',') if x_coordinates.count('NaN') > 0 else [],
                    y=y_coordinates.split(',') if y_coordinates.count('NaN') > 0 else [],
                )
                number_of_objects = question_drawn_response.x_coordinates.count('NaN')
            except QuestionDrawnResponse.DoesNotExist:
                x_coordinates = ''
                y_coordinates = ''
                pre_filled = dict(
                    x=[],
                    y=[],
                )
                number_of_objects = 0

            field_name = constants.FORM_QUESTION_PREFIX + job_question.id.__str__() \
                         + '_' + image_store.database_type.__str__()
            script, div = get_bokeh_images(
                url=image_store.image.url,
                field_name=field_name,
                pre_filled=pre_filled,
            )
            divs.append(
                [
                    div,
                    field_name,
                    number_of_objects,
                    x_coordinates,
                    y_coordinates,
                ]
            )
            scripts.append(script)

        signal_objects.append(ClassifyObject(
            questions=[q],
            divs=divs,
            scripts=scripts,
            visited=visited,
        ))

    return signal_objects