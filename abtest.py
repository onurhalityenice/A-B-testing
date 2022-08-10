#####################################################
# Comparison of Conversion of Bidding Methods with AB Test
#####################################################

# Variables:
# Impression: Ad views
# Click: Number of clicks on the displayed ad
# Purchase: Number of products purchased after ads clicked
# Earning: Earnings after purchased products

#####################################################
# Part 1:  Preparing and Analyzing Data
#####################################################

# Reading the data set ab_testing_data.xlsx consisting of control and test group data
# Assigning control and test group data to separate variables

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, \
    mannwhitneyu, pearsonr, spearmanr, kendalltau, f_oneway, kruskal

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel("Miuul/WEEK_4/ab_testing/ab_testing.xlsx", sheet_name="Control Group")
df_test= pd.read_excel("Miuul/WEEK_4/ab_testing/ab_testing.xlsx", sheet_name="Test Group")

df_control.describe()
df_test.describe()

# Combine the control and test group data using the concat method.
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()

#####################################################
# Part 2:  Defining the A/B Test Hypothesis
#####################################################

# Define the hypothesis

# H0 : M1 = M2 (There is no difference between the control group and test group purchasing averages.)
# H1 : M1!= M2 (There is a difference between the control group and test group purchasing averages.)

# Analyzing purchase averages for the control and test group
df.groupby("group").agg({"Purchase": "mean"})

#####################################################
# Part 3: Performing Hypothesis Testing
#####################################################

# Performing assumption checks

# Normality Assumption
# H0: Assumption of normal distribution is provided.
# H1: Assumption of normal distribution is not provided
# p < 0.05 H0 REJECTED
test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.5891
# HO cannot be rejected. The values of the control group provide the assumption of normal distribution.

# Variance Homogeneity :
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 REJECTED
test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.1083
# HO cannot be rejected. The values of the Control and Test groups provide the assumption of variance homogeneity.

# Since the assumptions are provided, an independent two-sample t-test (parametric test) should be performed.
# H0: M1 = M2 (There is no statistically significant difference between the control group and test group purchasing averages.)
# H1: M1 != M2 (There is a statistically significant difference between the control group and test group purchasing averages)
# p<0.05 HO REJECTED , p>0.05 HO CANNOT BE REJECTED
test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.3493
# HO cannot be rejected. There is no statistically significant difference between the purchasing averages of the control and test groups.


##############################################################
# Part 4 : Analysis of Results
##############################################################

# Since the means are compared in this analysis, if statistical assumptions are provided, \
# the T test should be performed, and if not, the mannwhitneyu test should be performed.
# Since the assumptions were provided, I decided to use the T test.

# According to the test results, there is no statistically significant difference between \
# the bidding type called "maximumbidding" and the average earnings provided by the new alternative "average bidding".

# In this case, there is no need for this change in the bidding system.


### THE END ###