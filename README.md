I have generated a fictitious dataset (containing 1000 datapoints).
To get an idea of instrumental variables and their utility in a causal model.

<img src="https://github.com/user-attachments/assets/ec5418df-936d-4bc3-baf3-a963f631ffce" height="200" width="300"/>

The image shows a graph containing an unobserved U node, this node represents the ability, to generate the neighbouring node's (education, income) data, the randomized ability value is used to generate the education and income datapoint. The voucher data is a random variable that influences education just like the (unobserved) ability node. Income is influenced by a factor 4 by education, and by a factor 2 by the unobserved ability.

The whole idea of this setup is to try to statistically guess the influence by education. As all random data is normally distributed, this should be possible.

The Python package dowhy is created for this kind of calculations.

## Finding an estimand

The first thing to do is to let dowhy attempt to find an estimand.

As the voucher is uninfluenced by the unobserved U node, and it influences education, it is a good estimand for the effect of education on income.

The output upon finding the estimand voucher looks like

Estimand type: EstimandType.NONPARAMETRIC_ATE

### Estimand : 1
Estimand name: backdoor
No such variable(s) found!

### Estimand : 2
Estimand name: iv
Estimand expression:
 ⎡                                            -1⎤
 ⎢    d              ⎛    d                  ⎞  ⎥
E⎢──────────(income)⋅⎜──────────([education])⎟  ⎥
 ⎣d[voucher]         ⎝d[voucher]             ⎠  ⎦
Estimand assumption 1, As-if-random: If U→→income then ¬(U →→{voucher})
Estimand assumption 2, Exclusion: If we remove {voucher}→{education}, then ¬({voucher}→income)

### Estimand : 3
Estimand name: frontdoor
No such variable(s) found!

