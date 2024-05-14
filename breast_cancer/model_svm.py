import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Chargement des données
data = pd.read_csv('breast_cancer_data.csv')

# Affichage 
print(data.head())

# Suppression de la colonne 'id'
data = data.drop('id', axis=1)

# Convertir les étiquettes 
data['diagnosis'] = data['diagnosis'].map({'B': 0, 'M': 1})

# Séparation 
X = data.drop('diagnosis', axis=1)
y = data['diagnosis']

# Division 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 4.  SVM
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# 5. Évaluation 
y_pred = svm.predict(X_test)



#  Matrice de confusion et  rapport 
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='d', cbar=False)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))
print("\nRapport de classification :")
print(classification_report(y_test, y_pred))

# Sauvegarder 
joblib.dump(svm, 'svm_model.pkl')
joblib.dump(scaler, 'scaler.pkl')


