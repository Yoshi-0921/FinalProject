from common import AbstractResource
from flask import request

from scipy import stats
import numpy as np

from . import api

class GBMplot(AbstractResource):
    END_POINTS = ['/mathfinance/gbmplot']

    @api.doc(params={
        's': {
            'type': 'float'
        },
        'scale': {
            'type': 'float'
        },
        'S0': {
            'type': 'float'
        },
        'ax_from': {
            'type': 'float'
        },
        'ax_to': {
            'type': 'float'
        }})
    def get(self):
        _s = request.args.get('s', default=None, type=float)
        _scale = request.args.get('scale', default=None, type=float)
        _S0 = request.args.get('S0', default=1.0, type=float)
        ax_from = request.args.get('ax_from', default=0.5, type=float)
        ax_to = request.args.get('ax_to', default=6, type=float)

        axis = _S0*np.linspace(ax_from, ax_to, 200)

        resp = {
            'axis': axis.tolist(),
            'yearly': []
        }

        # 1 to 20 years
        years = np.arange(1, 21)
        for year in years:
            s = _s*year
            scale = _scale**year
            dist = stats.lognorm(s=s, scale=scale)
            any_loss_prob = dist.cdf(1.0) - dist.cdf(0.0)
            np_pdf_vals = dist.pdf(axis)
            pdf_vals = (np_pdf_vals / np.max(np_pdf_vals)).tolist()

            reject_prob = 0.10
            q_ub = dist.ppf(q=1.0-reject_prob/2)
            q_lb = dist.ppf(q=reject_prob/2)
            exp_90pp = dist.expect(lb=q_lb, ub=q_ub, conditional=True)

            q_25 = dist.ppf(0.25)
            q_50 = dist.ppf(0.5)
            q_75 = dist.ppf(0.75)

            resp['yearly'].append({
                'pdf_vals': pdf_vals,
                'any_loss_prob': any_loss_prob,
                'exp_90pp': _S0*exp_90pp,
                'E': _S0*dist.expect(),
                'q25': _S0*q_25,
                'q50': _S0*q_50,
                'q75': _S0*q_75
            })

        return resp

class GBMWithEdgeworthPlot(AbstractResource):
    END_POINTS = ['/mathfinance/gbmEWplot']

    @api.doc(params={
        'mean': {
            'type': 'float'
        },
        'sig': {
            'type': 'float'
        },
        'skew': {
            'type': 'float'
        },
        'kurt': {
            'type': 'float'
        },
        'S0': {
            'type': 'float'
        },
        'year': {
            'type': 'float'
        }})
    def get(self):
        mean = request.args.get('mean', default=0.0, type=float)
        sig= request.args.get('sig', default=1.0, type=float)
        skew= request.args.get('skew', default=0.0, type=float)
        kurt= request.args.get('kurt', default=0.0, type=float)
        _S0 = request.args.get('S0', default=1.0, type=float)
        year= request.args.get('year', default=20, type=float)

        axis = _S0*np.linspace(0.1, 10, 200)

        resp = {
            'axis' : axis.tolist(),
            'pdf_vals': []
        }

        def edgeworth(samples, mu, sig, skew, kurt):
            H3 = lambda x: x**3 - 3*x
            H4 = lambda x: x**4 - 6*x**2 + 3
            z = (samples - mu) / sig
            val = stats.norm(mu, sig).pdf(samples)*(1 + 1/6*skew*H3(z) + 1/24*kurt*H4(z))
            s = np.sum(val) * (samples[1] - samples[0])
            val /= s
            return list(map(lambda x: x if x >= 1e-20 else 1e-20, val))

        def log_edgeworth(samples, mu, sig, skew, kurt):
            return edgeworth(np.log(samples), mu, sig, skew, kurt) / samples

        logpdfs = log_edgeworth(axis, (mean - 0.5*sig**2) * 250*year, sig**2 * (250*year), skew, kurt)
        resp['pdf_vals'] = logpdfs.tolist()

        return resp
