from _datetime import datetime
from _overlapped import NULL

from flask import Flask
from flask_jsonpify import jsonpify
from flask_restful import reqparse
from sklearn import metrics 
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from lightgbm import LGBMClassifier


import numpy as np
import pandas as pd
from lightgbm.sklearn import LGBMRegressor
from scipy import matrix
from binstar_client.tests.urlmock import unicode
from sklearn.model_selection._validation import cross_val_score
from lightgbm.compat import DataFrame
from cProfile import label


app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    
    train = pd.read_csv('./csvfile/results.csv')
    
  
    return NULL
    
   
    

    
    
if __name__ == '__main__': app.run()
    
    
    
    
    
    
