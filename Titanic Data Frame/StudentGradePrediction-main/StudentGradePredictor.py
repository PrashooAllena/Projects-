import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

class StudentGradePredictor:

    def __init__(self,data_path):
        self.data = pd.read_csv('student-mat.csv')

    def prepare_data(self):
        self.numeric_data = self.data.select_dtypes(include=['float64','int64'])

        self.X = self.numeric_data[['G1', 'G2']]
        self.y = self.numeric_data['G3']

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
    
    def train_model(self):
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)

    def predict(self, new_data):
        self.value = self.model.predict(new_data)[0]  

        if self.value > 100:
            self.value = 100
        elif self.value < 0:
            self.value = 0
            
        return self.value

