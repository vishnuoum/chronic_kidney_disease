# import libraries
from itsdangerous import exc
import joblib
import json
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import pytesseract

# load models
global DT,DNN,RF
DT=joblib.load("model/CKD_DT.pkl")
SVM=joblib.load("model/CKD_SVM.pkl")
DNN=load_model("model/CKD_DNN.h5")

# function to extract values from lab report
def extract(path):
    try:
        values={}
        keys=["BP","SG","Albumin","PC","PCC","BGR","BU","SC","sc","Sodium","Hb","PCV","WBC","RBC"]
        data=pytesseract.image_to_string(Image.open(path))
        for line in data.splitlines():
            # print(line)
            delete=[]
            for i in range(len(keys)):
                if(keys[i] in line):
                    values[keys[i].upper()]=line.split()[1]
                    delete.append(i)
            for i in delete:
                print(keys[i])
                del keys[i]
        print(values)
        return values
    except:
        return "error"

# function to predict
def estimate(data):
    predictions=[]
    
    predictions.append(DT.predict([data])[0])
    predictions.append(SVM.predict([data])[0])
    pred=DNN.predict([data])
    predictions.append(pred.round()[0])
    vote_1=0
    for i in predictions:
        if(i==1.0):
            vote_1=vote_1+1
    return "ckd" if vote_1==2 else "notckd"