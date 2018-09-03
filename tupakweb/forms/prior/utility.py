from collections import OrderedDict

from ...models import Signal, Prior

from ..dynamic.field import SELECT
from ..signal.signal_parameter import BBH_FIELDS_PROPERTIES

PRIOR_TYPES = Prior.CHOICES


def prior_type_field(field_name, field_value):
    name = field_name
    value = field_value.copy()
    value.update({
        'label': 'Type',
        'type': SELECT,
        'choices': PRIOR_TYPES,
        'extra_class': 'prior-type',
    })
    return name + '_type', value


def prior_fixed_field(field_name, field_value):
    name = field_name
    value = field_value.copy()

    value.update({
        'label': 'Value',
    })
    return name + '_fixed', value


def prior_min_field(field_name, field_value):
    name = field_name
    value = field_value.copy()

    value.update({
        'label': 'Min',
    })
    return name + '_min', value


def prior_max_field(field_name, field_value):
    name = field_name
    value = field_value.copy()

    value.update({
        'label': 'Max',
    })
    return name + '_max', value


def get_field_properties_by_signal_choice(signal_choice):
    field_properties = OrderedDict()
    fieldsets = dict()
    if signal_choice == Signal.BINARY_BLACK_HOLE:
        for name, value in BBH_FIELDS_PROPERTIES.items():
            fieldset_fields = []
            # setting up the type field
            name_for_field, value_for_filed = prior_type_field(name, value)
            field_properties.update({
                name_for_field: value_for_filed,
            })

            fieldset_fields.append(name_for_field)

            # setting up the fixed value field
            name_for_field, value_for_filed = prior_fixed_field(name, value)
            field_properties.update({
                name_for_field: value_for_filed,
            })

            fieldset_fields.append(name_for_field)

            # setting up the min value field
            name_for_field, value_for_filed = prior_min_field(name, value)
            field_properties.update({
                name_for_field: value_for_filed,
            })

            fieldset_fields.append(name_for_field)

            # setting up the max value field
            name_for_field, value_for_filed = prior_max_field(name, value)
            field_properties.update({
                name_for_field: value_for_filed,
            })

            fieldset_fields.append(name_for_field)

            fieldsets.update({
                BBH_FIELDS_PROPERTIES.get(name).get('label'): fieldset_fields,
            })

        return fieldsets, field_properties
