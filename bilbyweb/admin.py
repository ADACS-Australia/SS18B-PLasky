"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.contrib import admin

from .models import (
    Job,
    Data,
    DataParameter,
    Signal,
    SignalParameter,
    Prior,
    Sampler,
    SamplerParameter,
)


# Register your models here.
@admin.register(Job)
class Job(admin.ModelAdmin):
    list_display = ('name', 'description', 'status_display', 'user',)
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
    list_display = ('job', 'signal_choice', 'signal_model')
    search_fields = ['job__name', 'signal_choice', 'signal_model', ]


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
    list_display = ('job', 'name', 'prior_choice', 'fixed_value', 'uniform_min_value', 'uniform_max_value')
    search_fields = ['job', 'name', 'prior_choice', ]


@admin.register(Sampler)
class Sampler(admin.ModelAdmin):
    list_display = ('job', 'sampler_choice',)
    search_fields = ['job__name', 'sampler_choice', ]


@admin.register(SamplerParameter)
class SamplerParameter(admin.ModelAdmin):
    list_display = ('get_job', 'get_sampler', 'name', 'value')
    search_fields = ['name', 'value']

    def get_job(self, obj):
        return obj.sampler.job.name

    get_job.admin_order_field = 'sampler__job'  # Allows column order sorting
    get_job.short_description = 'Job'  # Renames column head

    def get_sampler(self, obj):
        return obj.sampler.sampler_choice

    get_sampler.admin_order_field = 'sampler'  # Allows column order sorting
    get_sampler.short_description = 'sampler'  # Renames column head
