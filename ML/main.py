import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
import argparse
import test

## your model path should takes the form as
Model_Path = '/home/hyliu/ML_Project/model.json'
## for TA's test
## you need to modify the class name to your student id.
## you also need to implement the predict function, which reads the .json file,
## calls your trained model and returns predict results as an ndarray
## the evaluation function is f1_score as follows:
'''
from sklearn.metrics import f1_score
    macro_f1 = f1_score(y_true, y_pred, average="macro")
'''
## the test

class PB21061215():
    def predict(self, data_path): 
        # a dummy system
        df=pd.read_excel(data_path)
        test.PreProcess(df)
        pred=test.Predict(df)
        return pred
## for local validation
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test scripts')
    parser.add_argument('--test_data_path', type=str,
                        default='/home/hyliu/ML_Project/testing_dataset.xls')
    args = parser.parse_args()
    test_data = pd.read_excel(args.test_data_path)
    true = np.array(test_data["RRR"])
    bot = PB21061215()
    pred = bot.predict(args.test_data_path)
    macro_f1 = f1_score(y_true=true, y_pred=pred, average="macro")
    print(macro_f1)