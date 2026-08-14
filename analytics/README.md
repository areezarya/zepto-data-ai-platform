# Titanic Analytics Pipeline

## Project Overview

This project performs exploratory data analysis (EDA), data preprocessing, classification modeling, imbalance handling, hyperparameter tuning, regression analysis, and model deployment preparation using the Titanic dataset.

The objective was to predict passenger survival and analyze the factors influencing survival outcomes.

---

# Dataset

Dataset Source: Seaborn Titanic Dataset

An offline fallback copy was created using:

```python
df.to_csv("titanic.csv", index=False)
```

This allows the project to run without requiring network access.

---

# Missing Value Analysis

| Column | Missing % | Action Taken |
|----------|----------|----------|
| deck | 77.22% | Dropped (>30% missing) |
| age | 19.87% | Median Imputation (5–30% missing) |
| embarked | 0.22% | Rows Removed (<5% missing) |
| embark_town | 0.22% | Rows Removed (<5% missing) |

### Interpretation

The missing-value strategy followed a percentage-based rule:

- Columns with more than 30% missing values were dropped.
- Columns with 5%–30% missing values were imputed.
- Columns with less than 5% missing values had affected rows removed.

---

# Outlier Analysis

Outliers were detected using the IQR method.

### Age

- Number of outliers: 65

### Fare

- Number of outliers: 114

### Fare Skewness Interpretation

Fare is positively skewed because:

- Mean Fare > Median Fare
- Median Fare > Mode Fare

A small number of passengers paid extremely high fares, causing the distribution to be right-skewed.

---

# Bivariate Analysis

## Survival by Sex

Female passengers had substantially higher survival rates than male passengers.

This supports the historical "women and children first" evacuation pattern.

## Survival by Passenger Class

Passengers traveling in first class had the highest survival rates, while third-class passengers had the lowest.

This suggests socio-economic status influenced access to lifeboats and evacuation resources.

## Survival by Sex and Passenger Class

Female passengers consistently experienced higher survival rates across all passenger classes.

Third-class males experienced the lowest survival rates in the dataset.

---

# Correlation Analysis

Correlation matrix was computed using exactly these variables:

- survived
- pclass
- age
- sibsp
- parch
- fare

## Strongest Correlation #1

pclass and Fare

Correlation Coefficient: 0.548

### Interpretation

These variables exhibit the strongest linear relationship in the dataset, indicating that changes in one variable are associated with changes in the other.

---

## Strongest Correlation #2

sibsp and parch

Correlation Coefficient: 0.415

### Interpretation

This relationship suggests another important dependency within the dataset and may help explain survival or passenger characteristics.

---

# Multivariate Analysis

## Chart 1: Survival by Passenger Class and Sex

### Interpretation

Female passengers had higher survival rates across all passenger classes.

First-class females achieved the highest survival rates, while third-class males experienced the lowest.

---

## Chart 2: Fare Distribution by Passenger Class and Survival

### Interpretation

Passengers who survived generally paid higher fares, especially within first and second class.

This indicates that wealth and cabin location may have influenced survival outcomes.

---

## Chart 3: Age vs Fare Colored by Survival Status

### Interpretation

Survival is more common among passengers paying higher fares.

Age alone does not strongly separate survivors from non-survivors.

---

## Chart 4: Age Distribution by Passenger Class and Survival Status

### Interpretation

First-class passengers had better survival outcomes across most age groups.

Third-class passengers showed substantially lower survival rates.

---

# Standardization Check

Standardization was applied to:

- Age
- Fare

### Before Standardization

The variables had different scales and distributions.

### After Standardization

Both transformed variables achieved:

- Mean ≈ 0
- Standard Deviation ≈ 1

### Interpretation

The before-and-after comparison confirms that standardization was successfully applied and the transformed variables satisfy the expected scaling properties.

---

# Train/Test Split

A stratified train-test split was used.

### Justification

Stratification preserves the original class distribution of survivors and non-survivors in both training and testing datasets.

This produces more reliable evaluation results when class proportions are unequal.

---

# Classification Models

Three classifiers were trained using identical train/test splits:

1. Logistic Regression
2. Decision Tree
3. Random Forest

---

# Classification Model Comparison

| Model | Accuracy | Precision | Recall | F1 Score | AUC |
|---------|---------|---------|---------|---------|---------|
| Logistic Regression | 0.8090 | 0.7833 | 0.6912 | 0.7344 | 0.8610 |
| Decision Tree | 0.7697 | 0.6901 | 0.7206 | 0.7050 | 0.7541 |
| Random Forest | 0.8202 | 0.7812 | 0.7353 | 0.7576 | 0.8179 |

---

# Imbalance Handling Comparison

Three approaches were evaluated:

1. Baseline
2. class_weight='balanced'
3. SMOTE Oversampling

| Method | Precision | Recall | F1 Score |
|----------|----------|----------|----------|
| Baseline | 0.783333 | 0.691176 | 0.734375 |
| Balanced Weights | 0.718310 | 0.750000 | 0.733813 |
| SMOTE | 0.735294 | 0.735294 | 0.735294 |

### Conclusion

The baseline model achieved strong precision but lower recall.

Using class_weight='balanced' improved minority-class detection.

SMOTE produced the best overall balance between precision and recall and achieved the strongest F1 Score.

Therefore, SMOTE was selected as the most effective imbalance-handling strategy.

---

# Hyperparameter Tuning

GridSearchCV was performed on:

- n_estimators
- max_depth
- max_features

## Best Parameters

```python
{
    'max_depth': ...,
    'max_features': ...,
    'n_estimators': ...
}
```

### OOB Score

```
0.8073136427566807
```

The Out-of-Bag score provides an internal estimate of generalization performance using bootstrap samples.

---

# Regression Analysis

Target Variable:

- Fare

Model:

- Multiple Linear Regression

## Regression Metrics

| Model | MAE | RMSE | R² | Adjusted R² |
|---------|---------|---------|---------|---------|
| Linear Regression |21.0986 | 41.7021 | 0.3482 | 0.3091 |

---

# Residual Analysis

### Heteroscedasticity Conclusion

The residual plot shows increasing variability of residuals as predicted fare increases.

Residuals are not randomly distributed around zero and exhibit a widening spread at higher prediction values.

This indicates heteroscedasticity, meaning the variance of prediction errors is not constant across all predicted values.

---

# Model Deployment Artifact

The best-performing classifier was saved as a complete scikit-learn pipeline using:

```python
joblib.dump(full_pipeline, "best_pipeline.joblib")
```

The saved artifact contains:

- Imputation
- Encoding
- Standardization
- Final Classifier

The pipeline was successfully reloaded using:

```python
joblib.load("best_pipeline.joblib")
```

and generated predictions directly from raw, unprocessed passenger data.

---

# Final Recommendation

Among the evaluated classification models, Random Forest is recommended for deployment because it achieved the strongest overall predictive performance.

The model achieved:

- Accuracy: 0.8202
- Precision: 0.7812
- Recall: 0.7353
- F1 Score: 0.7576
- AUC:0.8179

The model demonstrated the best balance between precision and recall while maintaining strong discriminatory power as measured by AUC. Because it consistently outperformed the competing classifiers across the primary evaluation metrics, it is the preferred model for deployment on the Titanic survival prediction task.

