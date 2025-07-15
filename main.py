import numpy as np
import pandas as pd
import patsy as ps
from matplotlib import pyplot as plt
from numpy.random import random
from scipy import stats
from statsmodels.sandbox.regression.gmm import IV2SLS
import os, sys
from dowhy import CausalModel
import matplotlib.image as mpimg
from sympy import symbols, diff
from data import get_data

np.random.seed(1)

do=1
#https://www.youtube.com/watch?v=nsr9eh-qVPg

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

if do==2:
        df = get_data()
        res_v_e=stats.linregress(df["voucher"], df["education"])
        res_v_i=stats.linregress(df["voucher"],df["income"])
        res_e_i = stats.linregress(df["education"], df["income"])

        plt.scatter(df["voucher"], df["education"])
        plt.plot(df["voucher"], res_v_e.intercept + res_v_e.slope * df['voucher'], 'r', label='voucher/education fitted line')
        plt.xlabel("voucher")
        plt.ylabel("education")
        plt.legend()
        plt.savefig("out/v_e")
        #plt.show()
        plt.clf()


        plt.scatter(df["voucher"], df["income"])
        plt.plot(df["voucher"], res_v_i.intercept + res_v_i.slope * df['voucher'], 'r', label='voucher/income fitted line')
        plt.xlabel("voucher")
        plt.ylabel("income")
        plt.legend()
        plt.savefig("out/v_i")
        plt.clf()

        plt.scatter(df["education"], df["income"])
        plt.plot(df["education"], res_e_i.intercept + res_e_i.slope * df['education'], 'r',
                 label='voucher/income fitted line')
        plt.xlabel("education")
        plt.ylabel("income")
        plt.legend()
        plt.savefig("out/e_i")
        #plt.show()

        cov_v_e = df['voucher'].cov(df['education'])
        cov_v_i = df['voucher'].cov(df['income'])
        print("estimate= cov('voucher',income')/cov('voucher',education')")
        print(cov_v_i/cov_v_e)

if do==3:
        df = get_data()
        res_v_e = stats.linregress(df["voucher"], df["education"])
        res_v_i = stats.linregress(df["voucher"], df["income"])

        voucher = symbols('voucher', real=True)
        f_v_e = res_v_e.intercept + (res_v_e.slope * voucher)
        d_v_e = diff(f_v_e, voucher)
        #print(d)

        f_v_i = res_v_i.intercept + (res_v_i.slope * voucher)
        d_v_i = diff(f_v_i, voucher)
         #print(d2)

        print(d_v_i / d_v_e)





