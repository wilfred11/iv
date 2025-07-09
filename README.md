I have generated a fictitious dataset (containing 1000 datapoints).
To get an idea of instrumental variables and their utility in a causal model.

<img src="https://github.com/user-attachments/assets/ec5418df-936d-4bc3-baf3-a963f631ffce" height="200" width="300"/>

The image shows a graph containing an unobserved U node, this node represents the ability, to generate the neighbouring node's (education, income) data, the randomized ability value is used to generate the education and income datapoint. The voucher data is a random variable that influences education just like the (unobserved) ability node. Income is influenced by a factor 4 by education, and by a factor 2 by the unobserved ability.

The whole idea of this setup is to try to statistically guess the influence by education. As all random data is normally distributed, this should be possible.

The Python package dowhy is created for this kind of calculations.

### Finding an estimand

The first thing to do is to let dowhy attempt to find an estimand.

As the voucher node is uninfluenced by the unobserved U node, and it influences education, it is a good estimand for the effect of education on income. 

The code to find an estimand looks like 

`identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)`

The output upon finding the estimand voucher looks like below. The estimand assumptions made for the voucher estimand are true, as our data was created according to these premises. To calculate the effect education has on income when influencing education through voucher will be done via a combination of two partial derivatives.

Estimand type: EstimandType.NONPARAMETRIC_ATE

#### Estimand : 1
Estimand name: backdoor
No such variable(s) found!

#### Estimand : 2
Estimand name: iv

Estimand expression:

Expectation(Derivative(income, [voucher])*Derivative([education], [voucher])**(-1))

Estimand assumption 1, As-if-random: If U→→income then ¬(U →→{voucher})

Estimand assumption 2, Exclusion: If we remove {voucher}→{education}, then ¬({voucher}→income)

#### Estimand : 3
Estimand name: frontdoor
No such variable(s) found!

### Estimate the effect

To estimate the effect the following code is used.

`estimate = model.estimate_effect(identified_estimand, method_name="iv.instrumental_variable", test_significance=True)`

#### Realized estimand
Realized estimand: Wald Estimator

Realized estimand type: EstimandType.NONPARAMETRIC_ATE

Estimand expression:

Expectation(Derivative(income, [voucher])*Derivative([education], [voucher])**(-1))

Estimand assumption 1, As-if-random: If U→→income then ¬(U →→{voucher})

Estimand assumption 2, Exclusion: If we remove {voucher}→{education}, then ¬({voucher}→income)

Estimand assumption 3, treatment_effect_homogeneity: Each unit's treatment ['education'] is affected in the same way by common causes of ['education'] and ['income']

Estimand assumption 4, outcome_effect_homogeneity: Each unit's outcome ['income'] is affected in the same way by common causes of ['education'] and ['income']

Target units: ate

### Effect

The estimated effect of education on income is 4.01, which is very close to the value used when generating the data, the value used was 4. This effect indicates that increasing education by 1 increases income by 4.

#### Estimate
Mean value: 4.012529417821327
p-value: [0, 0.001]

### Refutation

`ref = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter", placebo_type="permute")`

Replacing the instrumental variable with an independent random variable reduces the effect to 













