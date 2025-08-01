To get an idea of instrumental variables and their utility in a causal model, a fictitious dataset is generated (containing 1000 datapoints).

<img src="https://github.com/user-attachments/assets/ec5418df-936d-4bc3-baf3-a963f631ffce" height="200" width="300"/>

The image shows a causal model containing an unobserved U node, this node represents the individual's ability. To generate the neighbouring nodes' (education, income) data, the randomized ability value is used to generate the education and income datapoints. The voucher data is a random variable that influences education just like the (unobserved) ability node. Income is influenced by a factor 4 by education, and by a factor 2 by the unobserved ability.

The whole idea of this setup is to try to statistically estimate the influence on income by education.

# The instrumental variable

As the unobserved variable (U) has a direct influence on income and on education, the education variable cannot be directly used to estimate its influence on income.

## The relevance assumption, the exclusion restriction, exogeneity assumption

The instrumental variable 'voucher' should have a direct causal influence on 'education', this is called **the relevance assumption**. Through the influence on 'education' it has influence on the 'income' variable. But it has no direct causal effect on income, this is **the exclusion restriction**. If it would have this direct effect on 'income', it would be hard to separate this effect from the effect the treatment 'education' has on 'income'. The corelation between 'voucher' and 'income' might just reflect some unobserved confounder, so that's why the instrumental variable should be randomly assigned to the unit, which is the **exogeneity assumption**.

## Visual relation between 'voucher' and 'education' and 'voucher' and 'income'.

The direct relation between variables voucher and education and voucher and income can be visualized.

<img width="325" alt="v_e" src="https://github.com/user-attachments/assets/e6b8ca22-45d7-4c53-9f5d-4cd23f07d7cb" />

<img width="325" alt="v_i" src="https://github.com/user-attachments/assets/b61c2100-8526-4c8b-b9cd-320b24efb37d" />

<img width="325" alt="e_i" src="https://github.com/user-attachments/assets/624a332a-0617-4091-b4c0-aa2eaace9789" />

## DoWhy package

Even though in this case it is fairly simple to calculate the effect, the dowhy package is a good option for estimating the effect a variable has on another variable. It also allows for the application of refutation tests.

## Calculating estimated effect by hand

### Using covariances

To calculate the effect, this piece of code is enough. The data variable represents a pandas dataframe. In this case the effect is calculated using a fraction of covariances. 

`cov_v_e = data['voucher'].cov(data['education'])`

`cov_v_i = data['voucher'].cov(data['income'])`

`estimated_effect=cov_v_i/cov_v_e`

### Using linear regression and derivatives

Another way to calculate the effect is using derivatives of linear regression lines' functions.

To calculate the regression lines for columns voucher and education, and voucher and income.

**calculating linear regression**

`from scipy import stats`

`res_v_e = stats.linregress(data["voucher"], data["education"])`

`res_v_i = stats.linregress(data["voucher"], data["income"])`

The values for these regression lines will be used to setup formulas for the lines. 

**calculating derivatives**

Sympy is a python package which allows to calculate derivatives for formulas.

`from sympy import symbols, diff`

`voucher = symbols('voucher', real=True)`

`f_v_e = res_v_e.intercept + (res_v_e.slope * voucher)`

`d_v_e = diff(f_v_e, voucher)`

`f_v_i = res_v_i.intercept + (res_v_i.slope * voucher)`

`d_v_i = diff(f_v_i, voucher)`

`estimated_effect=d_v_i / d_v_e`

### Using DoWhy

The first thing to do is to let dowhy attempt to find an estimand.

As the voucher node is uninfluenced by the unobserved U node, and it influences education, it is a good estimand for the effect of education on income. 

The code to find an estimand looks like 

`identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)`

Some output upon finding the estimand voucher looks like below. No frontdoor or backdoor variable is found. The expression by which to calculate the estimated effect is emitted. Some assumptions are also being expressed.

Estimand type: EstimandType.NONPARAMETRIC_ATE

#### Estimand : 2

Estimand name: iv

Estimand expression:

Expectation(Derivative(income, [voucher])*Derivative([education], [voucher])**(-1))

Estimand assumption 1, As-if-random: If U→→income then ¬(U →→{voucher})

Estimand assumption 2, Exclusion: If we remove {voucher}→{education}, then ¬({voucher}→income)

#### Estimate the effect

To estimate the effect the following code is used.

`estimate = model.estimate_effect(identified_estimand, method_name="iv.instrumental_variable", test_significance=True)`

**Realized estimand**

Realized estimand: Wald Estimator

Realized estimand type: EstimandType.NONPARAMETRIC_ATE

Estimand assumption, treatment_effect_homogeneity: Each unit's treatment ['education'] is affected in the same way by common causes of ['education'] and ['income']

Estimand assumption, outcome_effect_homogeneity: Each unit's outcome ['income'] is affected in the same way by common causes of ['education'] and ['income']

Target units: ate

**Effect**

The estimated effect of education on income is 4.101007007046957, which is close to the value used when generating the data, the value used was 4. 
This effect value indicates that increasing education by 1 increases income by 4.10, some p-value is given too (0.001)..

#### Refutation

[dowhy Refutation methods](https://causalwizard.app/inference/article/bootstrap-refuters-dowhy#:~:text=The%20refutation%20methods%20in%20DoWhy,with%20the%20model%20or%20data.)

Whereas ML's validation more broadly seeks to estimate model performance on unseen data, refutation seeks to do this by modelling the results of specific, defined scenarios. Each refutation scenario “disproves” a potential “explanation” of the original estimate. 

The Placebo Treatment refuter verifies that if you replace your real Treatment (education) with a random variable, the causal effect disappears.

Failing the Placebo-Treatment refuter suggests a methodological or program error, data-leakage, or data which easily allows a falsely non-zero causal effect to be generated. You should definitely investigate if this happens.

The test itself is applied like this

`ref = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter", placebo_type="permute")`

The code above results in the output below.

##### Placebo

The effect after applying the placebo refutation is 0, with a p-value of 0.92. According to this refutation test the original effect should be kept.

Refute: Use a Placebo Treatment

Estimated effect: 4.101007007046957

New effect: 0.02668550867867409

p value:0.8799999999999999

























