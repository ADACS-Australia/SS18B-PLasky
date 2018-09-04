from django.contrib import admin

from .models import (
    Job,
    Data,
    DataParameter,
    Signal,
    SignalParameter,
    Prior,
    Sampler,
    SamplerDynesty,
    SamplerEmcee,
    SamplerNestle,
)

# Register your models here.
admin.site.register(Sampler)
admin.site.register(SamplerDynesty)
admin.site.register(SamplerEmcee)
admin.site.register(SamplerNestle)


@admin.register(Job)
class Job(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'user',)
    search_fields = ['name', 'description', 'user__username', 'user__first_name', 'user__last_name', ]


@admin.register(Data)
class Data(admin.ModelAdmin):
    list_display = ('job', 'data_choice',)
    search_fields = ['job__name', 'data_choice', ]


@admin.register(DataParameter)
class DataParameter(admin.ModelAdmin):
    list_display = ('get_job', 'get_data', 'name', 'value')
    search_fields = ['name', 'value']

    def get_job(self, obj):
        return obj.data.job.name

    get_job.admin_order_field = 'data__job'  # Allows column order sorting
    get_job.short_description = 'Job'  # Renames column head

    def get_data(self, obj):
        return obj.data.data_choice

    get_data.admin_order_field = 'data'  # Allows column order sorting
    get_data.short_description = 'data'  # Renames column head


@admin.register(Signal)
class Signal(admin.ModelAdmin):
    list_display = ('job', 'signal_choice',)
    search_fields = ['job__name', 'signal_choice', ]


@admin.register(SignalParameter)
class SignalParameter(admin.ModelAdmin):
    list_display = ('get_job', 'get_signal', 'name', 'value')
    search_fields = ['name', 'value']

    def get_job(self, obj):
        return obj.signal.job.name

    get_job.admin_order_field = 'signal__job'  # Allows column order sorting
    get_job.short_description = 'Job'  # Renames column head

    def get_signal(self, obj):
        return obj.signal.signal_choice

    get_signal.admin_order_field = 'signal'  # Allows column order sorting
    get_signal.short_description = 'Signal'  # Renames column head


@admin.register(Prior)
class Prior(admin.ModelAdmin):
    list_display = ('get_job', 'get_signal', 'signal_parameter', 'prior_choice', 'fixed_value', 'uniform_min_value',
                    'uniform_max_value')
    search_fields = ['signal_parameter', 'get_signal', 'get_job']

    def get_job(self, obj):
        return obj.signal_parameter.signal.job.name

    get_job.admin_order_field = 'signal__job'  # Allows column order sorting
    get_job.short_description = 'Job'  # Renames column head

    def get_signal(self, obj):
        return obj.signal_parameter.signal.signal_choice

    get_signal.admin_order_field = 'signal'  # Allows column order sorting
    get_signal.short_description = 'Signal'  # Renames column head
