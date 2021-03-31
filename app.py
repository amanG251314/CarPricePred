from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('model/model.pickle', 'rb'))
encoders=pickle.load(open('model/encoders.pickle', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    #Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Mileage=float(request.form['Mileage'])
        City=(request.form['City'])
        State=(request.form['State'])
        Make=(request.form['Make'])
        Model=(request.form['Model'])
        print(City)
        #Preprocessing-----------------
        City=encoders['l_City_encoder'].transform([City])[0]
        #print(City)
        State=encoders['l_State_encoder'].transform([" "+State])[0]
        Make=encoders['l_Make_encoder'].transform([Make])[0]
        print(Make)
        Model=encoders['l_Model_encoder'].transform([Model])[0]
        #-------------------------------
        prediction=model.predict([[Year,Mileage,City,State,Make,Model]])
        output=round(prediction[0],2)
        print(output)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=False)

