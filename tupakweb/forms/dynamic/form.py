from django import forms

TEXT = 'text'
TEXT_AREA = 'text-area'
SELECT = 'select'
RADIO = 'radio'


def get_text_input(label, required, placeholder=None, initial=None):
    return forms.CharField(
        label=label,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': placeholder if placeholder else '',
            }
        ),
        required=required,
        initial=initial,
    )


def get_text_area_input(label, placeholder=None, initial=None, required=None):
    return forms.CharField(
        label=label,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': placeholder if placeholder else '',
            }
        ),
        required=True if required else False,
        initial=initial,
    )


def get_radio_input(label, choices=None, initial=None):
    # if not choices:
    #     # choices = DEFAULT_CHOICES
    #     # initial = DEFAULT_INITIAL

    return forms.ChoiceField(
        label=label,
        widget=forms.RadioSelect,
        choices=choices,
        initial=initial,
    )


def get_number_input(label):
    return forms.CharField(
        label=label,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )


def get_select_input(label, choices=None, initial=None):
    # if not choices:
    #     choices = DEFAULT_CHOICES
    #     initial = DEFAULT_INITIAL

    return forms.ChoiceField(
        label=label,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=choices,
        initial=initial,

    )


class DynamicForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # name of the form
        self.name = kwargs.pop('name')
        # dictionary of fields, each containing field_name as key, field_type, placeholder, choices etc. as values
        self.fields_properties = kwargs.pop('fields_properties')

        # request might be needed
        self.request = kwargs.pop('request', None)

        super(DynamicForm, self).__init__(*args, **kwargs)

        for name, properties in self.fields_properties.items():
            print(name, properties)

            if properties.get('type') == TEXT:
                self.fields[name] = get_text_input(
                    label=name,
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                )

            elif properties.get('type') == TEXT_AREA:
                self.fields[name] = get_text_area_input(
                    label=name,
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                )

    def clean_fields(self):
        print('I am here')
        pass
