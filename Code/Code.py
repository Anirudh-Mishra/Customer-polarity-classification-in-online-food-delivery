import numpy as np
import pandas as pd

data = pd.read_csv('data.csv')
data

data.describe()

data.isnull().sum()

data.columns
dropCol = ['latitude', 'longitude','Educational Qualifications','Pin code','Reviews']
data.drop(dropCol, axis = 1, inplace=True)

data.head()

import scipy.stats as st 

# Correlation values for variables more than a threshold of 0.4
corr=[]
for i in data.columns:
    if i not in  ['latitude','longitude','Pin code','Output','Reviews']:
        df=pd.crosstab(data['Output'],data[i])
        stat, p, dof, expected = st.chi2_contingency(df,correction=True)
        t=min(df.shape)-1
        deno=sum(df.sum())*t
        x=np.sqrt(stat / deno)
        if(x>0.4): #thresold
             corr.append((i,x))
corr

# # Visualisation of Age
# keysAge = data['Age'].unique()
# usersAge = []
# valuesYesAge = []
# valuesNoAge = []
# keysAge.sort()
# for i in keysAge:
#   usersAge.append((data['Age'] == i).sum())

# df = data.groupby(['Age', 'Output'])
# d = df.size().to_frame('size')

# d.reset_index(inplace = True)

# ageYesValues = []
# ageNoValues = [0]
# for i in range(0, 29, 2):
#   ageYesValues.append(d['size'][i])

# for i in range(1, 30, 2):
#   ageNoValues.append(d['size'][i])

# ageYesValues.append(0)
# plt.figure(figsize=(10,8))
# plt.bar(keysAge-0.2, ageYesValues, width = 0.4)
# plt.bar(keysAge+0.2, ageNoValues, width = 0.4)
# plt.legend(["Yes", "No"])

ax = data.groupby(['Age']).Output.value_counts().reset_index(name='counts').pivot(index='Age', columns='Output', values='counts').plot(kind='bar', figsize = (12,7))

ax = data.groupby(['Ease and convenient']).Output.value_counts().reset_index(name='counts').pivot(index='Ease and convenient', columns='Output', values='counts').plot(kind='bar', 
                                                                                                                                                                    figsize = (12,7))

ax = data.groupby(['Time saving']).Output.value_counts().reset_index(name='counts').pivot(index='Time saving', columns='Output', values='counts').plot(kind='bar', figsize = (12,7))

ax = data.groupby(['Easy Payment option']).Output.value_counts().reset_index(name='counts').pivot(index='Easy Payment option', columns='Output', values='counts').plot(kind='bar', figsize = (12,7))

ax = data.groupby(['More Offers and Discount']).Output.value_counts().reset_index(name='counts').pivot(index='More Offers and Discount', columns='Output', values='counts').plot(kind='bar', 
                                                                                                                                                                                 figsize = (12,7))

ax = data.groupby(['Good Food quality']).Output.value_counts().reset_index(name='counts').pivot(index='Good Food quality', columns='Output', values='counts').plot(kind='bar', figsize = (12,7))

ax = data.groupby(['Good Tracking system']).Output.value_counts().reset_index(name='counts').pivot(index='Good Tracking system', columns='Output', values='counts').plot(kind='bar', figsize = (12,7))

ax = data.groupby(['Unaffordable']).Output.value_counts().reset_index(name='counts').pivot(index='Unaffordable', columns='Output', values='counts').plot(kind='bar', figsize = (12,7))

ax = data.groupby(['More restaurant choices']).Output.value_counts().reset_index(name='counts').pivot(index='More restaurant choices', columns='Output', 
                                                                                                      values='counts').plot(kind='bar', figsize = (12,7))

ax = data.groupby(['Maximum wait time']).Output.value_counts().reset_index(name='counts').pivot(index='Maximum wait time', columns='Output', values='counts').plot(kind='bar', figsize = (12,7))

from sklearn.preprocessing import LabelEncoder
#Label Encoding

data.columns
colsEnc = ['Gender', 'Marital Status', 'Occupation', 'Monthly Income', 'Medium (P1)', 'Medium (P2)', 
           'Meal(P1)', 'Meal(P2)', 'Perference(P1)', 'Perference(P2)', 'Ease and convenient', 
           'Time saving', 'More restaurant choices', 'Easy Payment option', 'More Offers and Discount', 
           'Good Food quality', 'Good Tracking system', 'Self Cooking', 'Health Concern', 
           'Late Delivery', 'Poor Hygiene', 'Bad past experience', 'Unavailability', 'Unaffordable', 
           'Long delivery time', 'Delay of delivery person getting assigned',
           'Delay of delivery person picking up food', 'Wrong order delivered',
           'Missing item', 'Order placed by mistake', 'Influence of time', 'Order Time', 'Maximum wait time', 
           'Residence in busy location', 'Google Maps Accuracy', 'Good Road Condition', 'Low quantity low time', 
           'Delivery person ability', 'Influence of rating', 'Less Delivery time','High Quality of package', 
           'Number of calls', 'Politeness', 'Freshness ', 'Temperature', 'Good Taste ', 'Good Quantity', 'Output']

from sklearn.preprocessing import LabelEncoder

data[colsEnc] = data[colsEnc].apply(LabelEncoder().fit_transform)

data.head()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt

fig = plt.figure(figsize=[20, 18])
sns.heatmap(data.corr(method='spearman'), annot=False, mask=np.triu(data.corr(method='spearman')), cmap='Spectral',
            linewidths=0.1, linecolor='white')

data.shape

# Splitting the examples
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data.iloc[:, 0:49], data['Output'], test_size=0.25, random_state=42)

"""Logistic Regression"""

# import the class
from sklearn.linear_model import LogisticRegression

# instantiate the model (using the default parameters)
logreg = LogisticRegression()

# fit the model with data
logreg.fit(X_train,y_train)

#Predict the response for test dataset
y_pred=logreg.predict(X_test)

# import the metrics class
from sklearn import metrics
from sklearn.metrics import accuracy_score
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
cnf_matrix


from sklearn.metrics import classification_report
confusion_matrix = pd.crosstab(y_pred, y_test, rownames=['Prediction'], colnames=['Reference'])
print(confusion_matrix, end='\n\n')
print('Accuracy Score :',accuracy_score(y_test, y_pred), end='\n\n')
print('Classification Report : ')
print(classification_report(y_test, y_pred), end='\n\n')

# Confusion Matrix in heatmap format
class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

"""Naive Bayes"""

#Import Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB

#Create a Gaussian Classifier
gnb = GaussianNB()

#Train the model using the training sets
gnb.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = gnb.predict(X_test)

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

# Model Accuracy
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# import the metrics class
from sklearn import metrics
from sklearn.metrics import accuracy_score
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

from sklearn.metrics import classification_report
confusion_matrix = pd.crosstab(y_pred, y_test, rownames=['Prediction'], colnames=['Reference'])
print(confusion_matrix, end='\n\n')
print('Accuracy Score :',accuracy_score(y_test, y_pred), end='\n\n')
print('Classification Report : ')
print(classification_report(y_test, y_pred), end='\n\n')

# Confusion Matrix in heatmap format
class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

"""K-Nearest Neighbour"""

from sklearn.neighbors import KNeighborsClassifier

knn_best = KNeighborsClassifier(n_neighbors=8, p=1)
knn_best.fit(X_train,y_train.values.ravel())
y_pred = knn_best.predict(X_test)
obs = y_test

# import the metrics class
from sklearn import metrics
from sklearn.metrics import accuracy_score
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
confusion_matrix = pd.crosstab(y_pred, y_test, rownames=['Prediction'], colnames=['Reference'])
print(confusion_matrix, end='\n\n')
print('Accuracy Score :',accuracy_score(y_test, y_pred), end='\n\n')
print(classification_report(y_test, y_pred), end='\n\n')

# Confusion Matrix in heatmap format
class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

"""Support Vector Machines"""

from sklearn.model_selection import GridSearchCV
from sklearn import svm

svm_best = svm.SVC(C=5, kernel='rbf')
svm_best.fit(X_train,y_train.values.ravel())
y_pred = svm_best.predict(X_test)

# import the metrics class
from sklearn import metrics
from sklearn.metrics import accuracy_score
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
confusion_matrix = pd.crosstab(y_pred, y_test, rownames=['Prediction'], colnames=['Reference'])
print(confusion_matrix, end='\n\n')
print('Accuracy Score :',accuracy_score(y_test, y_pred), end='\n\n')
print(classification_report(y_test, y_pred), end='\n\n')

# Confusion Matrix in heatmap format
class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

"""ANN"""

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=50)

import tensorflow.keras as keras
model = keras.Sequential([
	keras.layers.Dense(49, input_shape=(None, 49), activation='relu'),
  keras.layers.Dense(26, activation='relu'),
  keras.layers.Dense(11, activation='relu'),
  keras.layers.Dense(1, activation='sigmoid')
])

model.summary()

model.compile(optimizer='RMSprop',
              loss="binary_crossentropy",
              metrics=["accuracy"])

history = model.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_val, y_val))

loss_train = history.history['accuracy']
loss_val = history.history['val_accuracy']
epochs = range(1,51)
plt.plot(epochs, loss_train, 'g', label='Training accuracy')
plt.plot(epochs, loss_val, 'b', label='validation accuracy')
plt.title('Training and Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

model.evaluate(X_test, y_test)

y_pred = model.predict(X_test)
y_pred = y_pred.flatten()
for i in range(97):
  if(y_pred[i] > 0.5):
    y_pred[i] = 1
  else:
    y_pred[i] = 0

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
cnf_matrix

confusion_matrix = pd.crosstab(y_pred, y_test, rownames=['Prediction'], colnames=['Reference'])
print(confusion_matrix, end='\n\n')
print('Accuracy Score :',accuracy_score(y_test, y_pred), end='\n\n')
print('Classification Report : ')
print(classification_report(y_test, y_pred))

# Confusion Matrix in heatmap format
pred = []
for i in range(len(X_test)):
  if(model.predict(X_test.iloc[i].to_numpy().reshape(1,49)) > 0.5):
    pred.append(1)
  else:
    pred.append(0)
cnf_matrix1 = metrics.confusion_matrix(y_test, pred)
cnf_matrix1

class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Create heatmap
print()
sns.heatmap(pd.DataFrame(cnf_matrix1), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
