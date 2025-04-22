from flask import Flask, redirect, render_template, request, send_from_directory, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# from flask_login import login_required, current_user
# from models import db, User, DoctorProfile, Appointment
import pickle
import numpy as np
import pandas as pd
from datetime import datetime


# # Add to existing imports
# from flask_socketio import SocketIO, emit, join_room, leave_room
# import eventlet
# eventlet.monkey_patch()




# load databasedataset===================================
sym_des = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv('datasets/medications.csv')
diets = pd.read_csv("datasets/diets.csv")


# load model===========================================
svc = pickle.load(open('models/svc.pkl','rb'))


app = Flask(__name__)


# Initialize after app creation
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')




# SQL -------------
app.config['SECRET_KEY'] = ' SUPER-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()





# Register User
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not username or not password:
            return {'message': 'Missing username or password'}, 400
        if User.query.filter_by(username= username).first():
            return {'message': 'User already taken'}, 400
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 200


# Login User
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username= username).first()

        if user and user.password == password:
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        
        return {'message': 'Invalid credentials'}, 401


class ProtectedResource(Resource):
    # validate token
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {'message': f"hello user {current_user_id}, you accessed the protected resource"}, 200

# @app.route('/dashboard')
# @jwt_required()
# def dashboard():
#     current_user_id = get_jwt_identity()
#     user = User.query.get(current_user_id)
#     return render_template('dashboard.html', username=user.username)


@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return render_template('dashboard.html', username=user.username)
    else:
        return {'message': 'User not found'}, 404






api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/secure')


#

#============================================================
# custome and helping functions
#==========================helper funtions================
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis] ['workout']
    return desc,pre,med,die,wrkout


symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]


# creating routes==========================
@app.route('/')
def index():
    return render_template('index.html')

#////////////////////////////////////////////////////////////////////////////////////////
# # @app.route('/predict', methods=['GET', 'POST'])
# # def predict():
#     if request.method == 'POST':
#         symptoms = request.form.get('symptoms')
#         user_symptoms = [s.strip() for s in symptoms.split(',')]
#         # Remove any extra characters, if any
#         user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
#         predicted_disease = get_predicted_value(user_symptoms)
           
#         desc, pre, med, die, wrkout = helper(predicted_disease)

#         # my_precautions = []
#         # for i in precautions[0]:
#         #     my_precautions.append(i)

#         return render_template('index.html', predicted_disease=predicted_disease, dis_des=desc,
#             dis_pre=pre, dis_med=med, dis_wrkout=wrkout)

#     # return render_template('index.html')



@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        user_symptoms = [s.strip() for s in symptoms.split(',')]
        # Remove any extra characters
        user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
        
        # Validate symptoms
        valid_symptoms = [symptom for symptom in user_symptoms if symptom in symptoms_dict]

        if not valid_symptoms:
            # If no valid symptoms, return an error message
            return render_template('index.html', error="No valid symptoms provided. Please check your input.")

        try:
            predicted_disease = get_predicted_value(valid_symptoms)
            desc, pre, med, die, wrkout = helper(predicted_disease)
            return render_template(
                'index.html',
                predicted_disease=predicted_disease,
                dis_des=desc,
                dis_pre=pre,
                dis_med=med,
                dis_wrkout=wrkout,
                dis_die=die
            )
        except Exception as e:
            # Handle unexpected errors gracefully
            return render_template('index.html', error=f"An error occurred: {str(e)}")

    return render_template('index.html')


# /////////////////////////////////////////////////Session////////////////////////////////////////////////////


# @app.route('/video_call/<int:appointment_id>')
# @login_required
# def video_call(appointment_id):
#     appointment = Appointment.query.get_or_404(appointment_id)
    
#     # Verify participant
#     if current_user.id not in [appointment.doctor_id, appointment.patient_id]:
#         abort(403)
    
#     # Create or get video session
#     video_session = VideoSession.query.filter_by(appointment_id=appointment_id).first()
#     if not video_session:
#         video_session = VideoSession(
#             appointment_id=appointment_id,
#             session_id=f"VID-{appointment_id}-{datetime.now().timestamp()}"
#         )
#         db.session.add(video_session)
#         db.session.commit()
    
#     return render_template('video_call.html',
#                          appointment=appointment,
#                          session_id=video_session.session_id,
#                          current_user_id=current_user.id)






# # Add these after your routes
# @socketio.on('connect')
# def handle_connect():
#     print(f"Client connected: {request.sid}")

# @socketio.on('join_room')
# def handle_join(data):
#     room = data['room']
#     join_room(room)
#     emit('user_connected', {'peer_id': request.sid}, room=room, include_self=False)

# @socketio.on('signal')
# def handle_signal(data):
#     emit('signal', {
#         'signal': data['signal'],
#         'peer_id': request.sid
#     }, room=data['room'], include_self=False)

# @socketio.on('disconnect')
# def handle_disconnect():
#     print(f"Client disconnected: {request.sid}")







# ////////////////////////////////////////////////////////////////////////////////////////


@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# @app.route('/developer')
# def developer():
#     return render_template('developer.html')

@app.route('/login')
def login():
    # Render the login template
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True)
