from copy import deepcopy
import statsmodels.api as sm
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample


# Won't work for singular matrix (Singular matrix = Matrix whose determinant is zero)
def arima(window_values):
    weighted_window_vaues = deepcopy(window_values)
    weights = [0.06, 0.07, 0.08, 0.09, 0.1, 0.1, 0.11, 0.12, 0.13, 0.14]
    for x in range(0, 10):
        weighted_window_vaues[x] *= weights[x]
    arma_mod = sm.tsa.ARMA(weighted_window_vaues, order=(0, 0))
    arma_res = arma_mod.fit()
    # print(arma_res.summary())

    res = arma_res
    params = res.params
    residuals = res.resid
    p = res.k_ar
    q = res.k_ma
    k_exog = res.k_exog
    k_trend = res.k_trend
    steps = 1

    return _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend,
                                       k_exog, endog=weighted_window_vaues, exog=None, start=len(weighted_window_vaues)) * 10


'''
if __name__ == '__main__':
    # value = arima([12, 12, 12, 12, 12, 12, 12, 12, 12, 20])
    # value = arima([150, 150, 150, 150, 150, 150, 150, 150, 150, 160])
    # value = arima([900, 950, 980, 920, 990, 910, 940, 960, 950, 990])
    value = arima([61.62, 68.25, 78.24, 72.99, 97.0, 89.80000000000001, 113.96, 114.83999999999999, 118.95, 135.94000000000003])

    print(value)
'''
