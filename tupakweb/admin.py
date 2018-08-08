from django.contrib import admin

from .models import (
    Job,
    Data,
    DataOpen,
    DataSimulated,
    Signal,
    SignalBbhParameter,
    Prior,
    PriorFixed,
    PriorUniform,
    Sampler,
    SamplerDynesty,
    SamplerEmcee,
    SamplerNestle,
)

# Register your models here.
admin.site.register(Job)
admin.site.register(Data)
admin.site.register(DataOpen)
admin.site.register(DataSimulated)
admin.site.register(Signal)
admin.site.register(SignalBbhParameter)
admin.site.register(Prior)
admin.site.register(PriorFixed)
admin.site.register(PriorUniform)
admin.site.register(Sampler)
admin.site.register(SamplerDynesty)
admin.site.register(SamplerEmcee)
admin.site.register(SamplerNestle)
