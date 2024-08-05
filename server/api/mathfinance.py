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
        ax_to = request.args.get('ax_to', default=4, type=float)

        axis = _S0*np.linspace(ax_from, ax_to, 30)

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
            pdf_vals = dist.pdf(axis).tolist()

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
