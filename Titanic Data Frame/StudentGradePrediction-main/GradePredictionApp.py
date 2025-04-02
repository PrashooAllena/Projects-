import streamlit as st
import pandas as pd 

class GradePredictionApp:

    def __init__(self, predictor):
        self.predictor = predictor
    
    def run(self):
        st.title("Student Grade Prediction")
        st.write("Enter your previous grades(G1 and G2) and predict the final grade")

        g1 = st.number_input("Enter G1 (previous grade 1)", min_value=0, max_value= 100)
        g2 = st.number_input("Enter G2 (previous grade 2)", min_value=0, max_value= 100)

        if st.button("Predict the grade"):
            new_data = pd.DataFrame({'G1':[g1], 'G2':[g2]})
            predicted_grade = self.predictor.predict(new_data)
            st.success(f"Predicted Grade: {predicted_grade:.2f}")
