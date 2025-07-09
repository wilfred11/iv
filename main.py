import numpy as np
import pandas as pd
import patsy as ps

from statsmodels.sandbox.regression.gmm import IV2SLS
import os, sys
from dowhy import CausalModel
import matplotlib.image as mpimg

from data import get_data

do=1

if do==1:
        df=get_data()
        print(df.head())

        #Step 1: Model
        model=CausalModel(
                data = df,
                treatment='education',
                outcome='income',
                common_causes=['U'],
                instruments=['voucher']
                )
        #model.view_model(file_name="out/model", layout="dot")

        identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
        print(identified_estimand)

        # Choose the second estimand: using IV
        estimate = model.estimate_effect(identified_estimand,
                                         method_name="iv.instrumental_variable", test_significance=True)

        print(estimate)

        # Step 4: Refute
        ref = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter",
                                    placebo_type="permute")  # only permute placebo_type works with IV estimate
        print(ref)

