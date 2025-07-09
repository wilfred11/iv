import numpy as np
import pandas as pd


def get_data():
    n_points = 1000
    education_abilty = 1
    education_voucher = 2
    income_abilty = 2
    income_education = 4
    # confounder
    ability = np.random.normal(0, 3, size=n_points)

    # instrument
    voucher = np.random.normal(2, 1, size=n_points)

    # treatment
    education = np.random.normal(5, 1, size=n_points) + education_abilty * ability + \
                education_voucher * voucher

    # outcome
    income = np.random.normal(10, 3, size=n_points) + \
             income_abilty * ability + income_education * education

    # build dataset (exclude confounder `ability` which we assume to be unobserved)
    data = np.stack([education, income, voucher]).T
    df = pd.DataFrame(data, columns=['education', 'income', 'voucher'])

    return df