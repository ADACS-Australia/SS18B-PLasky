from collections import OrderedDict

from ...models import Signal, Prior

from ..dynamic.field import SELECT
from ..signal.signal_parameter import BBH_FIELDS_PROPERTIES

PRIOR_TYPES = Prior.CHOICES


def prior_type_field(field_name, field_value):
    name = field_name
    value = field_value.copy()
    value.update({
        'label': value.get('label') + ' type',
        'type': SELECT,
        'choices': PRIOR_TYPES,
    })
    return name + '_type', value


def prior_fixed_field(field_name, field_value):
    name = field_name
    value = field_value.copy()

    value.update({
        'label': 'Fixed',
    })
    return name + '_fixed', value


def get_field_properties_by_signal_choice(signal_choice):
    field_properties = OrderedDict()
    if signal_choice == Signal.BINARY_BLACK_HOLE:
        for name, value in BBH_FIELDS_PROPERTIES.items():
            # setting up the type field
            name_for_type, value_for_type = prior_type_field(name, value)
            field_properties.update({
                name_for_type: value_for_type,
            })

            # setting up the fixed value field
            name_for_fixed, value_for_fixed = prior_fixed_field(name, value)
            field_properties.update({
                name_for_fixed: value_for_fixed,
            })
        return field_properties
