# generic.py
import pickle

def load_model():
    # Load your trained model
    with open('trained_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model
