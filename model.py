import psycopg2
import itertools

DB_NAME = "skyforge"
DB_USER = "kolden"
DB_PASS = "Jaswanthsudharsan007"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
      conn = psycopg2.connect(database=DB_NAME,
                              user=DB_USER,
                              password=DB_PASS,
                              host=DB_HOST,
                              port=DB_PORT)
      print("Database connected successfully")
except Exception as e:
      print("Database not connected successfully")
      print(e)

cur = conn.cursor()

cur.execute("select column_name from information_schema.columns where table_name = 'public2';")
response = cur.fetchall()
#print(response)

import pandas as pd
df = pd.read_csv('/home/kolden/Documents/Github/Skyforge/venv/output.csv')

df['radiant_win'] = df['radiant_win'].str.strip()
df['radiant_win'] = df['radiant_win'].replace(to_replace=['True','False'],value=[0,1])

column_names = list(itertools.chain(*response))
column_names.remove("radiant_win")
column_names.remove("id")
column_names.remove("index")
#print(column_names)

X = df[column_names]
Y = df.radiant_win

correlation_matrix = df.corr()
#correlation_matrix.to_csv('corr.csv')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
X_train, X_test, y_train, y_test = train_test_split(X, Y , test_size = 0.25, random_state=17)

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(random_state=16)
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)

from sklearn import metrics

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

from sklearn.metrics import classification_report
target_names = ['Radiant win', 'Dire victory']
clr_report = classification_report(y_test, y_pred, target_names=target_names,output_dict=True)
print(classification_report(y_test, y_pred, target_names=target_names))

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# sns.heatmap(cnf_matrix, 
#             annot=True,
#             fmt='g', 
#             xticklabels=['Radiant Victory','Dire Victory'],
#             yticklabels=['Radiant Victory','Dire Victory'])
# plt.title('Confusion Matrix', fontsize=17, pad=20)
# plt.gca().xaxis.set_label_position('top') 
# plt.xlabel('Prediction', fontsize=13)
# plt.gca().xaxis.tick_top()

# plt.gca().figure.subplots_adjust(bottom=0.2)
# plt.gca().figure.text(0.5, 0.05, 'Prediction', ha='center', fontsize=13)
# plt.show()

def plot_classification_report(report):
    labels = list(report.keys())[:-3]  # Exclude 'accuracy', 'macro avg', 'weighted avg'
    values = [report[label]['precision'] for label in labels] + [report[label]['recall'] for label in labels] + [report[label]['f1-score'] for label in labels]
    labels = ['Precision']*len(labels) + ['Recall']*len(labels) + ['F1-Score']*len(labels)
    metrics = list(report.keys())[:-3] * 3
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(metrics, values, color=['blue', 'green', 'red']*len(report.keys()))
    ax.set_xlabel('Scores')
    ax.set_title('Classification Report')
    plt.tight_layout()
    plt.show()

plot_classification_report(clr_report)