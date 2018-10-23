#!/bin/python
"""
"""
from __future__ import division, print_function
import bilby
import json
import sys


def create_prior(name, prior):
    """ Conversion tool from dictionary-prior to bilby-prior """
    if prior['type'] == 'fixed':
        return prior['value']
    elif prior['type'] == 'uniform':
        return bilby.prior.Uniform(prior['min'], prior['max'], name)


with open(sys.argv[1], 'r') as file:
    job = json.load(file)

print(job)

duration = float(job['data']['signal_duration'])
sampling_frequency = 2048.

outdir = sys.argv[2]
label = job['name'].replace(' ', '_')

# Sets up some default parameters
injection_parameters = dict(
    mass_1=36., mass_2=29., a_1=0.4, a_2=0.3, tilt_1=0.5, tilt_2=1.0,
    phi_12=1.7, phi_jl=0.3, luminosity_distance=2000., iota=0.4, psi=2.659,
    phase=1.3, geocent_time=1126259642.413, ra=1.375, dec=-1.2108)

# Overwrite the defaults with those from the job (eventually should just use the input)
injection_parameters.update(job['signal'])

waveform_arguments = dict(waveform_approximant='IMRPhenomPv2',
                          reference_frequency=50.)

waveform_generator = bilby.gw.WaveformGenerator(
    duration=duration, sampling_frequency=sampling_frequency,
    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
    parameters=injection_parameters, waveform_arguments=waveform_arguments)
hf_signal = waveform_generator.frequency_domain_strain()

IFOs = []
detector_map = dict(hanford='H1', livingston='L1', virgo='V1')
for name in eval(job['data']['detector_choice']):
    det = detector_map[name]
    IFOs.append(
        bilby.gw.detector.get_interferometer_with_fake_noise_and_injection(
            det, injection_polarizations=hf_signal,
            injection_parameters=injection_parameters, duration=duration,
            sampling_frequency=sampling_frequency, outdir=outdir))

# Set up some default priors
priors = bilby.gw.prior.BBHPriorSet()
priors['geocent_time'] = bilby.core.prior.Uniform(
    minimum=injection_parameters['geocent_time'] - 1,
    maximum=injection_parameters['geocent_time'] + 1,
    name='geocent_time', latex_label='$t_c$')
for key in ['a_1', 'a_2', 'tilt_1', 'tilt_2', 'phi_12', 'phi_jl']:
    priors[key] = injection_parameters[key]

for key in job['priors']:
    priors[key] = create_prior(key, job['priors'][key])

likelihood = bilby.gw.GravitationalWaveTransient(
    interferometers=IFOs, waveform_generator=waveform_generator,
    time_marginalization=False, phase_marginalization=False,
    distance_marginalization=False, prior=priors)

result = bilby.run_sampler(
    likelihood=likelihood, priors=priors,
    injection_parameters=injection_parameters, outdir=outdir, label=label,
    sampler=job['sampler']['type'],
    npoints=int(float(job['sampler']['number_of_live_points'])))

result.plot_corner()
