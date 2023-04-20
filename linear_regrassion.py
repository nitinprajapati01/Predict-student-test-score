# -*- coding: utf-8 -*-
"""PM_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F_kpT87aI790LNjGeXP6zPxGe_hgHX7V
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import os
        
# Config
mpl.rcParams['font.family'] = 'sans-serif' 
sns.set_theme(style="white", palette=None)
plt.rcParams["figure.figsize"] = (16,7.5)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

"""# **1. Load data**"""

df = pd.read_csv("test_scores.csv")
df.head()

df = df.set_index("student_id")

print("Shape:", df.shape)

df.describe().T

"""Check for null values"""

df.isna().sum()

"""Change some solumns dtype Float to Integer"""

df[["n_student", "pretest", "posttest"]] = df[["n_student", "pretest", "posttest"]].astype("int64")
#df.dtypes

"""# 2. Quick **summary**"""

print("Number of student in this dataset:", len(df))
male_pct = np.round(len(df[df.gender=="Male"])/len(df)*100, 1)
print("Male: {0}\nFemale: {1}".format(male_pct, 100 - male_pct))

print("There are {0} schools with {1} different types among {2} regions".format(len(df["school"].unique()),
                                                                                len(df["school_type"].unique()),
                                                                                len(df["school_setting"].unique())
                                                                               )
     )
     
print("There are {0} classes with {1} different teaching method and {2} different lunch quality".format(
    len(df["classroom"].unique()),
    len(df["teaching_method"].unique()),
    len(df["school_setting"].unique()))
     )

"""**School:**

Number of school: **23**
Type of school: **Public** or **Non-public**
Region of school: **Urban**, **Suburban** or **Rural**

**Class:**

Number of class: **97**
Teaching method: **Standard** or **Experimental**
Lunch quality: **different among classes in the same school**, can be **Does not qualify** or **Qualifies for reduced/free** lunch
Number of students in class: about **14-31 students** per class.

**Student:**

Number of student: **2133**
Gender percentage:

Male **50.5%**
Female 49.5%

# 3. Quick **EDA**

Distribution of posttest score
"""

bar_color="#027ffc"
# plot 
fig = sns.histplot(data=df,
                   x="posttest",
                   kde=True,
                   stat="probability",
                   color=bar_color
                  );

plt.title("Distribution of post-test score", fontweight="bold", fontsize=18)
plt.xlabel("Score")

"""Count-plot of categoric variables."""

categoric_vars = ['school', 'school_setting', 'school_type', 'teaching_method', 'gender', 'lunch']

fig, ax = plt.subplots(figsize=(20,12), nrows=2, ncols=3)

plt.suptitle("Qiuck count plot for categoric variables", fontweight="bold", fontsize=16)

for c, axis in zip(categoric_vars, ax.ravel()):
    sns.countplot(data=df, x=c, ax=axis)

"""Average post-test score by school's features"""

avgscore_school = df.groupby(by=["school_setting",
                                 "school_type"], observed=True)["posttest"].mean().round(1).sort_values().reset_index()

palette = sns.color_palette("hls", 8)

# plot 
fig = sns.barplot(data=avgscore_school,
                  x="school_setting", y="posttest",
                  hue = "school_type",
                  palette = palette,
                  orient='v',
                  dodge=.8
                  );

plt.title("Average post-test score by school's features", fontweight="bold", fontsize=16)
plt.xlabel("Region")
plt.ylabel("Post-test score")

fig.bar_label(fig.containers[0]);
fig.bar_label(fig.containers[1]);

"""Average post-test score by classroom's features"""

avgscore_classroom = df.groupby(by=["teaching_method", "lunch"])["posttest"].mean().round(1).reset_index()

# plot 
fig = sns.barplot(data=avgscore_classroom,
                  x="teaching_method", y="posttest",
                  hue = "lunch",
                  palette = palette,
                  orient='v',
                  dodge=.8
                  );

plt.title("Average post-test score by classroom features", fontweight="bold", fontsize=16)
plt.xlabel("Teaching method")
plt.ylabel("Post-test score")

fig.bar_label(fig.containers[0]);
fig.bar_label(fig.containers[1]);

"""Number of student per class and post-test score"""

def create_bin(x):
    if x<20:
        return "<20"
    elif 20<=x<25:
        return "20-25"
    elif 25<=x<30:
        return "25-30"
    else:
        return "30+"

df["n_student_bin"] = df["n_student"].apply(create_bin)

fig = sns.barplot(data=df,
                  x="n_student_bin",
                  estimator=np.mean,
                  y="posttest",
                  color=bar_color
                );

"""Pretest and Posttest"""

fig, ax = plt.subplots(figsize=(20,18), nrows=3, ncols=2)

for c, axis in zip(categoric_vars[1:], ax.ravel()):
    sns.scatterplot(data=df,
                    x="pretest", y="posttest",
                    hue=c,
                    ax=axis
                   )
    
ax[2][1].set_visible(False)

"""Correlation plot"""

df_corr = df.corr().transpose()

fig = plt.figure(figsize=(8,5))
gs = fig.add_gridspec(1,1)
gs.update(wspace=0.3, hspace=0.15)
ax0 = fig.add_subplot(gs[0,0])

# plot
color_palette = ["#5833ff","#da8829"]
mask = np.triu(np.ones_like(df_corr))
ax0.text(1.3,-0.1,"Correlation Matrix",fontsize=14, fontweight='bold', color="#000000")
sns.heatmap(df_corr,mask=mask,fmt=".3f",annot=True,cmap='Blues')

"""# 4. Build **model**

I'm trying to build simple model predict post-test score based on pre-test score only...

Split train and test data used by this model
"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

X_train, X_test, y_train, y_test = train_test_split(df["pretest"], df["posttest"],
                                                    test_size = 0.25, # use 25% data to test model
                                                    random_state=42
                                                   )
print("The shape of X_train is ", X_train.shape)
print("The shape of X_test is ",X_test.shape)
print("The shape of y_train is ",y_train.shape)
print("The shape of y_test is ",y_test.shape)

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

lr1 = LinearRegression()
lr1.fit(X_train.values.reshape(-1, 1), y_train)
y_pred = lr1.predict(X_test.values.reshape(-1, 1))
print("MSE: ", np.round(mean_squared_error(y_test, y_pred),3))
print("R-squared: ", np.round(r2_score(y_test, y_pred),3))

"""Let's build more complex regression model and compare...

Feature selection

First, we will select the variables that are likely affect the target variable (post-test score) inferred from EDA process:

1. school_setting
2. school_type
3. teaching_method
4. n_student_bin
5. lunch
6. pretest

Second, we need to encode categoric variables.
"""

df_train = df.copy()
var = ["school_setting", "school_type", "teaching_method", "n_student_bin", "lunch", "pretest", "posttest"]
df_train = df_train[var]

# Encoding data
from sklearn.preprocessing import OrdinalEncoder

X = df_train[var[:-1]]
y = df_train[var[-1]]

oe_encoder = OrdinalEncoder(dtype="int64")
X.iloc[:, :-1] = oe_encoder.fit_transform(X.iloc[:, :-1]).astype("int64")
X

# split
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.25, # use 25% data to test model
                                                    random_state=42
                                                   )
print("The shape of X_train is ", X_train.shape)
print("The shape of X_test is ",X_test.shape)
print("The shape of y_train is ",y_train.shape)
print("The shape of y_test is ",y_test.shape)

def regression_report(y_true, y_pred):
    from sklearn.metrics import mean_absolute_error, mean_squared_error, max_error, median_absolute_error, r2_score, explained_variance_score
    import numpy as np
    error = y_true - y_pred
    percentil = [5,25,50,75,95]
    percentil_value = np.percentile(error, percentil)
    
    metrics = [
        ('mean absolute error', mean_absolute_error(y_true, y_pred)),
        ('median absolute error', median_absolute_error(y_true, y_pred)),
        ('mean squared error', mean_squared_error(y_true, y_pred)),
        ('max error', max_error(y_true, y_pred)),
        ('r2 score', r2_score(y_true, y_pred)),
        ('explained variance score', explained_variance_score(y_true, y_pred))
    ]
    
    print('Metrics for regression:')
    for metric_name, metric_value in metrics:
        print(f'{metric_name:>25s}: {metric_value: >20.3f}')
        
    print('\nPercentiles:')
    for p, pv in zip(percentil, percentil_value):
        print(f'{p: 25d}: {pv:>20.3f}')

lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

print("=============Linear Regression model============\n")
regression_report(y_test, y_pred)

"""Good, after select important features, Mean Squared Error on testing data went down to **10.7** and R-squared improved to 0.945

Regressors with variable selection
"""

from sklearn.linear_model import ElasticNet, Lasso, LassoCV, Lars, LarsCV

regr = ElasticNet()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)

print("=============ElasticNET Regression model============\n")
regression_report(y_test, y_pred)

regr = LassoCV()
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)

print("=============LassoCV Regression model============\n")
regression_report(y_test, y_pred)

# Function: if score >100, return 100
limit = lambda x: 100 if x>100 else x
vect_limit = np.vectorize(limit)

# Map to y_pred
y_pred = vect_limit(np.round(lr.predict(X_test),1))

# Create result
result = X_test.copy()
result["Actual post-test score"] = y_test
result["Predited post-test score"] = y_pred

result.head(20)

result.to_csv("PredictStudentScore_LinearRegression.csv")

