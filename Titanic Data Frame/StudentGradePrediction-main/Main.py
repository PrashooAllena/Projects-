import StudentGradePredictor
import GradePredictionApp
import streamlit as st

predictor = StudentGradePredictor.StudentGradePredictor("student-mat.csv")
predictor.prepare_data()
predictor.train_model()

app = GradePredictionApp.GradePredictionApp(predictor)
app.run()