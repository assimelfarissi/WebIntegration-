from sklearn.tree import DecisionTreeClassifier
import pickle

X = [[50,200,1000],[1200,20,200],[300,80,500],[20,300,1500]]
y = ["High","Low","Medium","High"]

model = DecisionTreeClassifier()
model.fit(X,y)

with open("model.pkl","wb") as f:
    pickle.dump(model,f)
