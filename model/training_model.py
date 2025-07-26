import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, classification_report

# تحميل البيانات (استبدلي هذا بالملف الخاص بك إذا كان لديك CSV)
# df = pd.read_csv('your_file.csv')
# X = df.drop('label', axis=1)
# y = df['label']

# 👇 بيانات وهمية (استبدليها ببياناتك):
X = np.random.rand(100, 5)
y = np.random.choice(['bird', 'Drone'], size=100)

# تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# تدريب النموذج
model = SVC(kernel='rbf', probability=True)
model.fit(X_train, y_train)

# التنبؤ
y_pred = model.predict(X_test)

# حساب الدقة و F1 Score
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, pos_label='bird', average='binary')  # عدلي حسب التسمية

print("✅ Accuracy:", round(accuracy, 2))
# print("✅ F1 Score:", round(f1, 2))
# print("\n📋 Classification Report:")
# print(classification_report(y_test, y_pred))

# حفظ النتائج في DataFrame
results_df = pd.DataFrame({
    'True Label': y_test,
    'Predicted Label': y_pred
}).reset_index(drop=True)

# استخراج أول 3 نتائج متنوعة (طائر - درون - طائر)
selected = []
labels_used = []

for i, row in results_df.iterrows():
    label = row['Predicted Label']
    if len(selected) == 0:
        selected.append(row)
        labels_used.append(label)
    elif len(selected) == 1 and label != labels_used[0]:
        selected.append(row)
        labels_used.append(label)
    elif len(selected) == 2 and label == labels_used[0]:
        selected.append(row)
        break

# طباعة النتائج الثلاث المختارة
selected_df = pd.DataFrame(selected)
print("\n🔎 أول ثلاث نتائج متنوعة:")
print(selected_df)
