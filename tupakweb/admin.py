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
admin.site.register(Signal)
admin.site.register(SignalBbhParameter)
admin.site.register(Prior)
admin.site.register(PriorFixed)
admin.site.register(PriorUniform)
admin.site.register(Sampler)
admin.site.register(SamplerDynesty)
admin.site.register(SamplerEmcee)
admin.site.register(SamplerNestle)


@admin.register(Job)
class Job(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'user', )
    search_fields = ['name', 'description', 'user__username', 'user__first_name', 'user__last_name', ]


@admin.register(Data)
class Data(admin.ModelAdmin):
    list_display = ('job', 'data_choice', )
    search_fields = ['job__name', 'data_choice', ]


@admin.register(DataOpen)
class DataOpen(admin.ModelAdmin):
    list_display = ('job', 'detector_choice', 'signal_duration', 'sample_frequency', 'start_time', )
    search_fields = ['job__name', ]


@admin.register(DataSimulated)
class DataSimulated(admin.ModelAdmin):
    list_display = ('job', 'detector_choice', 'signal_duration', 'sample_frequency', 'start_time', )
    search_fields = ['job__name', ]
