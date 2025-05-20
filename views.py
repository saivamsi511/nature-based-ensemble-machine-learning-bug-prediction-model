from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import VotingClassifier
#model selection
from sklearn.metrics import confusion_matrix, accuracy_score, plot_confusion_matrix, classification_report
# Create your views here.




from Remote_User.models import ClientRegister_Model,bug_report_prediction,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_Bug_Report_Type(request):
    if request.method == "POST":

        if request.method == "POST":

            bug_id= request.POST.get('bug_id')
            creation_date= request.POST.get('creation_date')
            component_name= request.POST.get('component_name')
            product_name= request.POST.get('product_name')
            short_description= request.POST.get('short_description')
            long_description= request.POST.get('long_description')
            reporter_name= request.POST.get('reporter_name')
            resolution_category= request.POST.get('resolution_category')
            status_category= request.POST.get('status_category')
            bug_fix_time= request.POST.get('bug_fix_time')

        df = pd.read_csv('Datasets.csv')

        # data under nlp
        print("Data Processing Under Natural Language Processing (NLP)")
        data = []
        Labels = []
        

        def apply_results(results):
            if (results == 'normal'):
                return 0
            elif (results == 'blocker'):
                return 1
            elif (results == 'major'):
                return 2
            elif (results == 'minor'):
                return 3


        df['results'] = df['severity_category'].apply(apply_results)

        X = df['short_description']
        y = df['results']

        cv = CountVectorizer()
        x = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Naive Bayes")

        from sklearn.naive_bayes import MultinomialNB

        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes = accuracy_score(y_test, predict_nb) * 100
        print("ACCURACY")
        print(naivebayes)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_nb))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_nb))
        models.append(('naive_bayes', NB))

        # SVM Model
        print("SVM")
        from sklearn import svm

        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print("ACCURACY")
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('SVM', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression

        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('LogisticRegression', reg))

        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))
        models.append(('DecisionTreeClassifier', dtc))

        print("KNeighborsClassifier")
        from sklearn.neighbors import KNeighborsClassifier
        kn = KNeighborsClassifier()
        kn.fit(X_train, y_train)
        knpredict = kn.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, knpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knpredict))
        models.append(('KNeighborsClassifier', kn))

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        short_description1 = [short_description]
        vector1 = cv.transform(short_description1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = str(pred.replace("]", ""))

        prediction = int(pred1)

        if (prediction == 0):
            val = 'normal'
        elif (prediction == 1):
            val = 'blocker'
        elif (prediction == 2):
            val = 'major'
        elif (prediction == 3):
            val = 'minor'


        print(prediction)
        print(val)

        bug_report_prediction.objects.create(
        bug_id=bug_id,
        creation_date=creation_date,
        component_name=component_name,
        product_name=product_name,
        short_description=short_description,
        long_description=long_description,
        reporter_name=reporter_name,
        resolution_category=resolution_category,
        status_category=status_category,
        bug_fix_time=bug_fix_time,
        Prediction=val)

        return render(request, 'RUser/Predict_Bug_Report_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_Bug_Report_Type.html')



