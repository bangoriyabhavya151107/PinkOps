# PinkOps — Stage 4.1.1: Mathematical Derivation & Epistemic Foundation of the Lower Uncertainty Bound (LUB)
**Project:** Operation Pink Panther / PinkOps  
**Brand:** PinkOps  
**Stage:** Stage 4.1.1 Pre-Stage-5 Hardening  
**Status:** Formally Derived Mathematical Foundation  

---

## 1. Estimator Definition

Let $i \in \{1, \dots, M\}$ index players. For player $i$, let $Y_{ij}$ denote the observed value-added on delivery $j \in \{1, \dots, n_i\}$.
The observed sample mean performance rate is:

$$\bar{Y}_i = \frac{1}{n_i} \sum_{j=1}^{n_i} Y_{ij}$$

The Empirical Bayes (EB) shrinkage estimator $\hat{\mu}_{i, \text{EB}}$ shrinks the observed sample mean toward the population baseline $\mu_0 = 0.0$ (representing the league-average expectation):

$$\hat{\mu}_{i, \text{EB}} = \lambda_i \bar{Y}_i + (1 - \lambda_i) \mu_0$$

where $\lambda_i \in [0, 1]$ is the sample-dependent shrinkage weight.

---

## 2. Prior and Shrinkage Assumptions

We assume a hierarchical model where latent player talent parameters $\mu_i$ are drawn from a common population prior:

$$\mu_i \sim \mathcal{N}(\mu_0, \tau^2)$$

where:
- $\mu_0 = 0.0$ is the calibrated mean value-added across all competitive deliveries.
- $\tau^2 = \operatorname{Var}(\mu_i)$ represents the cross-sectional dispersion of true talent across the population of professional T20 cricketers.

The shrinkage parameter $K$ is defined as the variance ratio:

$$K = \frac{\sigma^2}{\tau^2}$$

which represents the effective number of "pseudo-deliveries" of prior information. The shrinkage weight is:

$$\lambda_i = \frac{\tau^2}{\tau^2 + \sigma^2 / n_i} = \frac{n_i}{n_i + K}$$

---

## 3. Sampling Model

Delivery-level performance outcomes $Y_{ij}$ conditional on player talent $\mu_i$ follow:

$$Y_{ij} \mid \mu_i \stackrel{\text{iid}}{\sim} \mathcal{D}(\mu_i, \sigma_i^2)$$

By the Central Limit Theorem, for moderate to large $n_i$, the distribution of the sample mean is:

$$\bar{Y}_i \mid \mu_i \approx \mathcal{N}\left(\mu_i, \frac{\sigma^2}{n_i}\right)$$

where $\sigma^2$ is the average delivery-level outcome variance (empirically measured as $\sigma = 1.10$).

---

## 4. Variance Derivation

We evaluate the precision of the estimator from two complementary statistical frameworks:

### 4.1 Frequentist Sampling Variance Conditional on Fixed $\mu_i$
Treating $\mu_i$ as a fixed unknown parameter:

$$\operatorname{Var}(\hat{\mu}_{i, \text{EB}} \mid \mu_i) = \operatorname{Var}\left(\lambda_i \bar{Y}_i + (1 - \lambda_i)\mu_0 \;\middle|\; \mu_i\right) = \lambda_i^2 \operatorname{Var}(\bar{Y}_i \mid \mu_i)$$

$$\operatorname{Var}(\hat{\mu}_{i, \text{EB}} \mid \mu_i) = \left(\frac{n_i}{n_i + K}\right)^2 \frac{\sigma^2}{n_i} = \frac{n_i \sigma^2}{(n_i + K)^2}$$

The frequentist bias is:

$$\operatorname{Bias}(\hat{\mu}_{i, \text{EB}} \mid \mu_i) = \mathbb{E}[\hat{\mu}_{i, \text{EB}} \mid \mu_i] - \mu_i = \lambda_i \mu_i + (1 - \lambda_i)\mu_0 - \mu_i = (1 - \lambda_i)(\mu_0 - \mu_i) = \frac{K(\mu_0 - \mu_i)}{n_i + K}$$

The frequentist Mean Squared Error (MSE) is:

$$\operatorname{MSE}(\hat{\mu}_{i, \text{EB}} \mid \mu_i) = \operatorname{Var}(\hat{\mu}_{i, \text{EB}} \mid \mu_i) + \operatorname{Bias}^2 = \frac{n_i \sigma^2}{(n_i + K)^2} + \frac{K^2 (\mu_i - \mu_0)^2}{(n_i + K)^2}$$

### 4.2 Bayesian Posterior Variance
Under conjugate Normal-Normal Bayesian updating:

$$\mu_i \mid \bar{Y}_i \sim \mathcal{N}\left(\lambda_i \bar{Y}_i + (1 - \lambda_i)\mu_0, \; \sigma_{i, \text{post}}^2\right)$$

The posterior precision is the sum of the data precision and prior precision:

$$\frac{1}{\sigma_{i, \text{post}}^2} = \frac{n_i}{\sigma^2} + \frac{1}{\tau^2} = \frac{n_i}{\sigma^2} + \frac{K}{\sigma^2} = \frac{n_i + K}{\sigma^2}$$

Inverting yields the exact posterior variance:

$$\sigma_{i, \text{post}}^2 = \operatorname{Var}(\mu_i \mid \bar{Y}_i) = \frac{\sigma^2}{n_i + K}$$

### 4.3 Total Expected Mean Squared Error (Bayes Risk)
Averaging the frequentist MSE across the population distribution of true talent $\mu_i \sim \mathcal{N}(\mu_0, \tau^2)$ where $\mathbb{E}[(\mu_i - \mu_0)^2] = \tau^2 = \sigma^2 / K$:

$$\mathbb{E}_{\mu}[\operatorname{MSE}(\hat{\mu}_{i, \text{EB}})] = \frac{n_i \sigma^2}{(n_i + K)^2} + \frac{K^2 (\sigma^2 / K)}{(n_i + K)^2} = \frac{n_i \sigma^2 + K \sigma^2}{(n_i + K)^2} = \frac{\sigma^2 (n_i + K)}{(n_i + K)^2} = \frac{\sigma^2}{n_i + K}$$

> **Key Theoretical Result:** The Bayesian posterior variance and the total expected MSE (Bayes Risk) of the Empirical Bayes estimator are mathematically identical: $\frac{\sigma^2}{n_i + K}$.

---

## 5. Standard Error Derivation

The standard error $\text{SE}_{\text{EB}}$ is defined as the root total expected Mean Squared Error:

$$\text{SE}_{i, \text{EB}} = \sqrt{\frac{\sigma^2}{n_i + K}}$$

### Limiting Boundary Behavior
1. **As $n_i \to 0$ (Zero Data / Pure Prior):**
   $$\text{SE}_{i, \text{EB}} \to \sqrt{\frac{\sigma^2}{K}} = \tau$$
   The standard error equals the population standard deviation of talent ($\tau \approx 0.11$). Uncertainty is bounded by the dispersion of the talent pool.
2. **As $n_i \to \infty$ (Asymptotic Sample):**
   $$\text{SE}_{i, \text{EB}} \to \frac{\sigma}{\sqrt{n_i}}$$
   The estimator smoothly converges to the classical standard error of the sample mean.

---

## 6. Bound Construction: Lower Uncertainty Bound (LUB)

The Lower Uncertainty Bound at coverage quantile $\alpha$ is constructed as:

$$\text{LUB}_{i, \alpha} = \hat{\mu}_{i, \text{EB}} - z_\alpha \cdot \text{SE}_{i, \text{EB}} = \hat{\mu}_{i, \text{EB}} - z_\alpha \sqrt{\frac{\sigma^2}{n_i + K}}$$

For our primary operating specification ($\alpha = 0.20$):

$$\text{LUB}_{i, 20} = \hat{\mu}_{i, \text{EB}} - 0.842 \sqrt{\frac{\sigma^2}{n_i + K}}$$

Alternative pre-registered quantiles:
- $\text{LUB}_{10}$: $z_{0.10} = 1.282$ (Strict risk-averse boundary)
- $\text{LUB}_{15}$: $z_{0.15} = 1.036$
- $\text{LUB}_{25}$: $z_{0.25} = 0.674$
- $\text{LUB}_{30}$: $z_{0.30} = 0.524$

---

## 7. Precise Epistemic Interpretation

### Valid Formulations (Scientific Standard)
- "Under the specified normal approximation and data-generating assumptions, the Lower Uncertainty Bound ($\text{LUB}_{20}$) provides a conservative lower estimate for the player's latent performance parameter."
- "Across the population of players with sample size $n_i$, the true talent parameter $\mu_i$ will exceed $\text{LUB}_{20}$ in approximately 80% of cases under the hierarchical data-generating process."
- "The bound explicitly penalizes small sample sizes by widening the discount subtracted from the shrunk estimate."

### Prohibited Overclaiming (Non-Compliant Formulations)
- *Do NOT write:* "There is an 80% probability that player $X$'s true skill is above this bound" (without specifying the prior distribution and data-generating process).
- *Do NOT write:* "This is a statistically guaranteed minimum performance floor."
- *Do NOT write:* "The bound proves unchokeability."

---

## 8. Underlying Model Assumptions

1. **Exchangeability of Prior:** Player latent talent parameters $\mu_i$ are exchangeable draws from a common normal prior before conditioning on covariates.
2. **Constant Within-Player Noise:** Outcome variance $\sigma^2$ is assumed approximately homoscedastic across players ($\sigma \approx 1.10$).
3. **Additive Value-Added Metric:** Value-added per ball $Y_{ij}$ is stationary across the delivery sample.

---

## 9. Methodological Limitations

1. **Extreme Talent Heavy Tails:** Real cricket distributions may exhibit slight skewness or kurtosis (heavy right tails for power hitters like Russell/Maxwell). Normal approximations in the tails may slightly underestimate extreme positive outliers.
2. **Heteroscedasticity:** Bowlers with specialized death-overs roles may have higher delivery-level variance than defensive middle-overs spinners.
3. **Role Conditioning:** The prior mean $\mu_0 = 0.0$ applies to the league average, but role-specific expectations may slightly alter prior centers.

---

## 10. Coverage Validation Summary

In independent Monte Carlo simulation testing ($N = 10,000$ synthetic players across $n \in [5, 500]$ and heteroscedastic noise):
- Overall empirical coverage of nominal 80% $\text{LUB}_{20}$: **$81.18\%$**.
- Coverage in Robust Tier ($n \ge 150$): **$80.45\%$**.
- Coverage in Moderate Tier ($50 \le n < 150$): **$81.60\%$**.
- Coverage in Sparse Tier ($n < 50$): **$81.82\%$**.

*Full empirical validation data and code lineage are detailed in [`outputs/stage_4_1_1_lub_validation.md`](file:///D:/PinkOps/outputs/stage_4_1_1_lub_validation.md).*

---

*End of Stage 4.1.1 Uncertainty Derivation Document.*
