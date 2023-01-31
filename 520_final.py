# -*- coding: utf-8 -*-
"""520 final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tF0pI6CEOeXZ-qfCJYCFYWE9aPbEtYUY

# Initialation
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import figure
import seaborn as sns
from sklearn.model_selection import KFold
from itertools import product, combinations
from collections import Counter
from sklearn.metrics import accuracy_score
import sklearn
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
kfold = KFold(n_splits=5)
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score, plot_confusion_matrix,roc_curve,auc

"""# Data loading"""

df = pd.read_csv("/content/data.csv")
df.head()

X=df.drop(['date','home_team','home_team_result','away_team','tournament'],axis=1)
y=df['home_team_result']
X
y

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
X_train.head()
y_train.head()

"""# Data exploration"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
sns.set(style='whitegrid', color_codes=True)
np.random.seed(sum(map(ord, 'categorical')))
X=df.drop(['date','home_team','home_team_result','away_team','tournament'],axis=1)
y=df['home_team_result']
xcorr = X.corr(method='pearson')

#Data overview
fig=plt.figure() 
ax = fig.add_subplot(1,1,1)
ax.hist(df['home_team_result']) 
plt.title('sum of home_team_result')
plt.xlabel('home_team_result')
plt.show()
fig=plt.figure() 
ax = fig.add_subplot(1,1,1)
ax.hist(df['home_team_fifa_rank'])
plt.title('home_team_fifa_rank')
plt.xlabel('home_team_fifa_rank')
plt.show()
fig=plt.figure() 
ax = fig.add_subplot(1,1,1)
ax.hist(df['away_team_fifa_rank']) 
plt.title('away_team_fifa_rank')
plt.xlabel('away_team_fifa_rank')
plt.show()

#correlation between different features
plt.figure(figsize=(7, 7),dpi=100)
sns.heatmap(data=xcorr,
           )

#correlation between feature and label
heatmap = sns.heatmap(df.corr()[['home_team_result']].sort_values(by='home_team_result', ascending=False), vmin=-1, vmax=1, annot=True, cmap='BrBG')

"""# Model"""

#Baseline: Decision Tree
tree_clf = DecisionTreeClassifier()
tree_clf.fit(X_train, y_train)
y_pred = tree_clf.predict(X_test)
print(tree_clf.score(X_train, y_train))
print(tree_clf.score(X_test, y_test))
cv_cross = cross_validate(tree_clf, X,y, cv=kfold,)
cv_cross['test_score'].mean()

cm = plot_confusion_matrix(tree_clf, X_test, y_test)
plt.xlabel('Predicted label')
plt.ylabel('True Label')
plt.title('Decision Tree')
print(f1_score(y_test, tree_clf.predict(X_test),average=None))

#Logistic Regression
lr = LogisticRegression(penalty='l2', solver='saga', multi_class = 'multinomial', fit_intercept=True, max_iter = 4000)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print(lr.score(X_train, y_train))
print(lr.score(X_test, y_test))
cv_cross = cross_validate(lr, X,y, cv=kfold,)
cv_cross['test_score'].mean()

cm = plot_confusion_matrix(lr, X_test, y_test)
plt.xlabel('Predicted label')
plt.ylabel('True Label')
plt.title('Logistic Regression')
print(f1_score(y_test, lr.predict(X_test),average=None))

#Random Forest
params_rf = {"max_depth": [20,30],
                "min_samples_split": [10,20],
                "max_leaf_nodes": [175,200],
                "min_samples_leaf": [5,10],
                "n_estimators": [250,300],
                 "max_features": ["sqrt"],
                }

rf = RandomForestClassifier(random_state=1)

rf_cv = GridSearchCV(rf, params_rf, cv = 3, n_jobs = -1, verbose = False)

rf_cv.fit(X_train, y_train)
rf = rf_cv.best_estimator_
print(rf.score(X_test, y_test))
cv_cross = cross_validate(rf, X,y, cv=kfold,) 
cv_cross['test_score'].mean()

print(rf_cv.best_estimator_)
print(rf.score(X_train, y_train))

cm = plot_confusion_matrix(rf, X_test, y_test)
plt.xlabel('Predicted label')
plt.ylabel('True Label')
plt.title('Random Forest')
print(f1_score(y_test, rf.predict(X_test),average=None))

#Gradient Tree Boosting
gb = GradientBoostingClassifier(random_state=5)

params = {"learning_rate": [0.1,0.3,0.5],
            "min_samples_split": [5,10],
            "min_samples_leaf": [5],
            "max_depth":[3],
            "max_features":["sqrt"],
            "n_estimators":[100]
         } 

gb_cv = GridSearchCV(gb, params, cv = 3, n_jobs = -1, verbose = False)

gb_cv.fit(X_train, y_train)
gb = gb_cv.best_estimator_
print(gb_cv.best_params_)
gb
print(gb.score(X_train, y_train))
print(gb.score(X_test, y_test))
cv_cross = cross_validate(gb, X,y, cv=kfold,)
cv_cross['test_score'].mean()

cm = plot_confusion_matrix(gb, X_test, y_test)
plt.xlabel('Predicted label')
plt.ylabel('True Label')
plt.title('Gradient Boosting')
print(f1_score(y_test, gb.predict(X_test),average=None))

#SVM
k = ['linear', 'poly', 'rbf', 'sigmoid']
c = [0.01, 0.1, 1, 10, 50]
for i in range(len(c)):
  for j in range(len(k)):
    print('C =', c[i], 'kernal =', k[j])
    svm_clf = SVC(C = c[i], kernel = k[j])
    svm_clf.fit(X_train, y_train)
    print(svm_clf.score(X_test, y_test))
    cv_cross = cross_validate(svm_clf, X,y, cv=kfold,)
    print(cv_cross['test_score'].mean

#best SVM parameter
svm_clf = SVC(C = 0.1, kernel = 'linear')
svm_clf.fit(X_train, y_train)
print(svm_clf.score(X_train, y_train))
print(svm_clf.score(X_test, y_test))
cv_cross = cross_validate(svm_clf, X,y, cv=kfold,)
print(cv_cross['test_score'].mean())

cm = plot_confusion_matrix(svm_clf, X_test, y_test)
plt.xlabel('Predicted label')
plt.ylabel('True Label')
plt.title('SVM')
print(f1_score(y_test, svm_clf.predict(X_test),average=None))

#Neural Network
al = [0.001, 0.01, 0.1, 1]
hid = [[50, 50, 50], [100, 100]]
sol = ['adam', 'sgd']
act = ['logistic', 'relu']
for i in range(len(al)):
  for j in range(len(hid)):
    for k in range(len(sol)):
      for l in range(len(act)):
        print('alpha =', al[i], 'hid =', hid[j], 'solver =', sol[k], 'activation =', act[l])
        NN_clf = MLPClassifier(alpha = al[i], hidden_layer_sizes = hid[j], solver = sol[k], activation = act[l], random_state=1, max_iter=300)
        NN_clf.fit(X_train, y_train)
        print(NN_clf.score(X_test, y_test))
        cv_cross = cross_validate(NN_clf, X,y, cv=kfold,)
        cv_cross['test_score'].mean()

#best Neural Network
NN_clf = MLPClassifier(alpha = 1, hidden_layer_sizes = [100, 100], solver = 'adam', activation = 'relu', random_state=1, max_iter=300)
NN_clf.fit(X_train, y_train)
print(NN_clf.score(X_train, y_train))
print(NN_clf.score(X_test, y_test))
cv_cross = cross_validate(NN_clf, X,y, cv=kfold,)
print(cv_cross['test_score'].mean())

cm = plot_confusion_matrix(NN_clf, X_test, y_test)
plt.xlabel('Predicted label')
plt.ylabel('True Label')
plt.title('Neural Network')
print(f1_score(y_test, NN_clf.predict(X_test),average=None))

"""# World Cup data loading"""

teams_df = pd.read_csv("/content/32teams.csv")
teams_df = teams_df.set_index(['home_team'])
teams_df.head()

group_df = pd.read_csv("/content/group.csv")
group_df.head()

"""# Group Stage Match Prediction

"""

margin = 0.1

world_cup = group_df.set_index(['home_team'])
world_cup['points'] = 0
world_cup['win_prob'] = 0
world_cup['expected points'] = 0
world_cup['rank'] = None
team_win_prob = {}
for country in group_df['home_team'].unique():
    team_win_prob[country] = list()

for group in set(group_df['Group']):
  print('___Group {}:___'.format(group))
  
  for home, away in combinations(group_df.query('Group == "{}"'.format(group)).values, 2):
    print("{} vs. {}: ".format(home[0], away[0], end= ""))
    home = home[0]
    away = away[0]

    row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

    row['home_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
    row['away_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
    row['home_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
    row['home_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
    row['home_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
    row['away_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
    row['away_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
    row['away_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
    row['importance'] = 1.

    row1 = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

    row1['home_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
    row1['away_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
    row1['home_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
    row1['home_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
    row1['home_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
    row1['away_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
    row1['away_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
    row1['away_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
    row1['importance'] = 1.  
    # Model Output
    home_win_prob = (gb.predict_proba(row)[:,2][0]+(1-gb.predict_proba(row1)[:,2][0]))/2
        
        
        
    # Saving Model Output
    world_cup.loc[home, 'win_prob'] += home_win_prob
    world_cup.loc[away, 'win_prob'] += 1-home_win_prob

    team_win_prob[home].append(home_win_prob)
    team_win_prob[away].append(1-home_win_prob)
        
    # Determining Win / Draw / Lose based on home_win_prob
    if home_win_prob <= 0.5 - margin:
        print("{} wins with {:.2f}".format(away, 1-home_win_prob))
        world_cup.loc[away, 'points'] += 3
        world_cup.loc[away, 'expected points'] += (1-home_win_prob) * 3
    elif home_win_prob > 0.5 - margin and home_win_prob < 0.5 + margin:
        print("Draw")
        world_cup.loc[home, 'points'] += 1
        world_cup.loc[away, 'points'] += 1
        world_cup.loc[home, 'expected points'] += home_win_prob * 1
        world_cup.loc[away, 'expected points'] += (1-home_win_prob) * 1
    elif home_win_prob >= 0.5 + margin:
        points = 3
        world_cup.loc[home, 'points'] += 3
        world_cup.loc[home, 'expected points'] += home_win_prob * 3
        print("{} wins with {:.2f}".format(home, home_win_prob))

for group in set(group_df['Group']):
  country = []
  win_rate = []
  for teams_info in group_df.query('Group == "{}"'.format(group)).values:
    team_name = teams_info[0]
    country.append(team_name)
    win_rate.append(world_cup.loc[team_name, 'win_prob'])
  sorted_index = np.argsort(win_rate)
  i = 1
  while i <= 4:
    world_cup.loc[country[sorted_index[-i]], 'rank'] = i
    i+=1

world_cup

"""# Round of 16"""

round_16 = world_cup[['Group', 'rank']]
round_16.drop(round_16[(round_16['rank'] > 2)].index, inplace=True)
for team in (round_16.index.values):
  round_16.loc[team,'home_team_fifa_rank'] = teams_df.loc[team, 'home_team_fifa_rank']
  round_16.loc[team, 'home_team_mean_defense_score'] = teams_df.loc[team, 'home_team_mean_defense_score']
  round_16.loc[team, 'home_team_mean_offense_score'] = teams_df.loc[team, 'home_team_mean_offense_score']
  round_16.loc[team, 'home_team_mean_midfield_score'] = teams_df.loc[team, 'home_team_mean_midfield_score']

round_16

world_cup16 = round_16[['Group', 'rank']]
world_cup16

round16_df = pd.read_csv("/content/round_16.csv")
result16_df = round16_df[['home', 'away']]
round16_df

result16_df['home_win'] = 0
result16_df['away_win'] = 0
result16_df['winner'] = None

for i in range(8):
  home = result16_df.loc[i, 'home']
  away = result16_df.loc[i, 'away']
  row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)
  row['home_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row['away_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row['home_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row['home_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row['home_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row['away_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row['away_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row['away_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row['importance'] = 1.

  row1 = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

  row1['home_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row1['away_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row1['home_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row1['home_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row1['home_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row1['away_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row1['away_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row1['away_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row1['importance'] = 1.
  # Model Output
  home_win_prob = (gb.predict_proba(row)[:,2][0]+(1-gb.predict_proba(row1)[:,2][0]))/2

  result16_df.loc[i, 'home_win'] += home_win_prob
  result16_df.loc[i, 'away_win'] += 1-home_win_prob
        
  if home_win_prob < 0.5:
        print("{} wins with {:.2f}".format(away, 1-home_win_prob))
        result16_df.loc[i, 'winner'] = away
  elif home_win_prob >= 0.5:
        print("{} wins with {:.2f}".format(home, home_win_prob))
        result16_df.loc[i, 'winner'] = home

result16_df

"""# Quarter Final"""

quarter_df = pd.read_csv("/content/quarter.csv")
result8_df = quarter_df[['home', 'away']]
quarter_df

result8_df['home_win'] = 0
result8_df['away_win'] = 0
result8_df['winner'] = None

for i in range(4):
  home = result8_df.loc[i, 'home']
  away = result8_df.loc[i, 'away']
  row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)
  row['home_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row['away_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row['home_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row['home_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row['home_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row['away_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row['away_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row['away_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row['importance'] = 1.

  row1 = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

  row1['home_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row1['away_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row1['home_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row1['home_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row1['home_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row1['away_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row1['away_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row1['away_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row1['importance'] = 1.
  # Model Output
  home_win_prob = (gb.predict_proba(row)[:,2][0]+(1-gb.predict_proba(row1)[:,2][0]))/2


  result8_df.loc[i, 'home_win'] += home_win_prob
  result8_df.loc[i, 'away_win'] += 1-home_win_prob
        
  if home_win_prob < 0.5:
        print("{} wins with {:.2f}".format(away, 1-home_win_prob))
        result8_df.loc[i, 'winner'] = away
  elif home_win_prob >= 0.5:
        print("{} wins with {:.2f}".format(home, home_win_prob))
        result8_df.loc[i, 'winner'] = home

result8_df

"""# Semi Final"""

semi_df = pd.read_csv("/content/semi.csv")
result4_df = semi_df[['home', 'away']]
semi_df

result4_df['home_win'] = 0
result4_df['away_win'] = 0
result4_df['winner'] = None

for i in range(2):
  home = result4_df.loc[i, 'home']
  away = result4_df.loc[i, 'away']
  row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)
  row['home_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row['away_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row['home_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row['home_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row['home_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row['away_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row['away_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row['away_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row['importance'] = 1.

  row1 = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

  row1['home_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row1['away_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row1['home_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row1['home_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row1['home_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row1['away_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row1['away_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row1['away_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row1['importance'] = 1.
  # Model Output
  home_win_prob = (gb.predict_proba(row)[:,2][0]+(1-gb.predict_proba(row1)[:,2][0]))/2

  result4_df.loc[i, 'home_win'] += home_win_prob
  result4_df.loc[i, 'away_win'] += 1-home_win_prob
        
  if home_win_prob < 0.5:
        print("{} wins with {:.2f}".format(away, 1-home_win_prob))
        result4_df.loc[i, 'winner'] = away
  elif home_win_prob >= 0.5:
        print("{} wins with {:.2f}".format(home, home_win_prob))
        result4_df.loc[i, 'winner'] = home

result4_df

"""# Final"""

final_df = pd.read_csv("/content/final.csv")
result2_df = final_df[['home', 'away']]
final_df

result2_df['home_win'] = 0
result2_df['away_win'] = 0
result2_df['winner'] = None

for i in range(1):
  home = result2_df.loc[i, 'home']
  away = result2_df.loc[i, 'away']
  row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)
  row['home_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row['away_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row['home_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row['home_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row['home_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row['away_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row['away_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row['away_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row['importance'] = 1.

  row1 = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

  row1['home_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row1['away_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row1['home_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row1['home_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row1['home_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row1['away_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row1['away_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row1['away_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row1['importance'] = 1.
  # Model Output
  home_win_prob = (gb.predict_proba(row)[:,2][0]+(1-gb.predict_proba(row1)[:,2][0]))/2

  result2_df.loc[i, 'home_win'] += home_win_prob
  result2_df.loc[i, 'away_win'] += 1-home_win_prob
        
  if home_win_prob < 0.5:
        print("{} wins with {:.2f}".format(away, 1-home_win_prob))
        result2_df.loc[i, 'winner'] = away
  elif home_win_prob >= 0.5:
        print("{} wins with {:.2f}".format(home, home_win_prob))
        result2_df.loc[i, 'winner'] = home

result2_df

"""# Semi-Final FIFA 2022"""

semi_df = pd.read_csv("/content/semi1.csv")
result4_df = semi_df[['home', 'away']]
semi_df

result4_df['home_win'] = 0
result4_df['away_win'] = 0
result4_df['winner'] = None

for i in range(2):
  home = result4_df.loc[i, 'home']
  away = result4_df.loc[i, 'away']
  row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)
  row['home_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row['away_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row['home_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row['home_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row['home_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row['away_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row['away_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row['away_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row['importance'] = 1.

  row1 = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

  row1['home_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row1['away_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row1['home_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row1['home_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row1['home_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row1['away_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row1['away_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row1['away_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row1['importance'] = 1.
  # Model Output
  home_win_prob = (gb.predict_proba(row)[:,2][0]+(1-gb.predict_proba(row1)[:,2][0]))/2

  result4_df.loc[i, 'home_win'] += home_win_prob
  result4_df.loc[i, 'away_win'] += 1-home_win_prob
        
  if home_win_prob < 0.5:
        print("{} wins with {:.2f}".format(away, 1-home_win_prob))
        result4_df.loc[i, 'winner'] = away
  elif home_win_prob >= 0.5:
        print("{} wins with {:.2f}".format(home, home_win_prob))
        result4_df.loc[i, 'winner'] = home

result4_df

"""# Final FIFA 2022"""

final_df = pd.read_csv("/content/final1.csv")
result2_df = final_df[['home', 'away']]
final_df

result2_df['home_win'] = 0
result2_df['away_win'] = 0
result2_df['winner'] = None

for i in range(1):
  home = result2_df.loc[i, 'home']
  away = result2_df.loc[i, 'away']
  row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)
  row['home_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row['away_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row['home_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row['home_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row['home_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row['away_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row['away_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row['away_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row['importance'] = 1.

  row1 = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]), columns=X_train.columns)

  row1['home_team_fifa_rank'] = teams_df.loc[away, 'home_team_fifa_rank']
  row1['away_team_fifa_rank'] = teams_df.loc[home, 'home_team_fifa_rank']
  row1['home_team_mean_defense_score'] = teams_df.loc[away, 'home_team_mean_defense_score']
  row1['home_team_mean_offense_score'] = teams_df.loc[away, 'home_team_mean_offense_score']
  row1['home_team_mean_midfield_score'] = teams_df.loc[away, 'home_team_mean_midfield_score']
  row1['away_team_mean_defense_score'] = teams_df.loc[home, 'home_team_mean_defense_score']
  row1['away_team_mean_offense_score'] = teams_df.loc[home, 'home_team_mean_offense_score']
  row1['away_team_mean_midfield_score'] = teams_df.loc[home, 'home_team_mean_midfield_score']
  row1['importance'] = 1.
  # Model Output
  home_win_prob = (gb.predict_proba(row)[:,2][0]+(1-gb.predict_proba(row1)[:,2][0]))/2

  result2_df.loc[i, 'home_win'] += home_win_prob
  result2_df.loc[i, 'away_win'] += 1-home_win_prob
        
  if home_win_prob < 0.5:
        print("{} wins with {:.2f}".format(away, 1-home_win_prob))
        result2_df.loc[i, 'winner'] = away
  elif home_win_prob >= 0.5:
        print("{} wins with {:.2f}".format(home, home_win_prob))
        result2_df.loc[i, 'winner'] = home

result2_df