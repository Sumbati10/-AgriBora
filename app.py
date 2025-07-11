from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
from functools import wraps
import os, requests

from functions import img_predict, get_diseases_classes, get_crop_recommendation, get_fertilizer_recommendation, soil_types, Crop_types, crop_list

app = Flask(__name__)
app.secret_key = 'b9ebef2dbae122fa9c4846eb2526de24'

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
dir_path = os.path.dirname(os.path.realpath(__file__))

# --------------------------
# LOGIN REQUIRED DECORATOR
# --------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth', mode='login'))
        return f(*args, **kwargs)
    return decorated_function

# --------------------------
# ROUTES
# --------------------------

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/crop-recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(map(float, to_predict_list.values()))
        result = get_crop_recommendation(to_predict_list)
        return render_template("recommend_result.html", result=result)
    return render_template('crop-recommend.html')


@app.route('/fertilizer-recommendation', methods=['GET', 'POST'])
@login_required
def fertilizer_recommendation():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(map(float, to_predict_list.values()))
        result = get_fertilizer_recommendation(
            num_features=to_predict_list[:-2],
            cat_features=to_predict_list[-2:]
        )
        return render_template("fertilizer-recommend.html", result=result)
    return render_template('fertilizer-recommend.html', 
                           soil_types=enumerate(soil_types),
                           crop_types=enumerate(Crop_types))


@app.route('/crop-disease', methods=['GET', 'POST'])
@login_required
def find_crop_disease():
    if request.method == "GET":
        return render_template('crop-disease.html', crops=crop_list)
    else:
        file = request.files["file"]
        crop = request.form["crop"]
        file_path = os.path.join(dir_path, 'uploads', secure_filename(file.filename))
        file.save(file_path)
        prediction = img_predict(file_path, crop)
        result = get_diseases_classes(crop, prediction)
        return render_template('disease-prediction-result.html', image_file_name=file.filename, result=result)


@app.route('/weather', methods=['GET', 'POST'])
@login_required
def weather():
    if request.method == 'POST':
        city = request.form['city']
        api_key = "96cd3e85fd1aa5bbbfc318b428373d8b"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get('cod') != 200:
            return render_template('weather.html', error=data.get("message", "City not found."))

        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
        return render_template('weather-result.html', weather=weather_data)
    return render_template('weather.html')


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/predict-crop', methods=['POST'])
@login_required
def predict_crop_ajax():
    try:
        data = request.json
        to_predict_list = list(map(float, [
            data['N'], data['P'], data['K'],
            data['temperature'], data['humidity'],
            data['phosphore'], data['rainfall']
        ]))
        result = get_crop_recommendation(to_predict_list)
        return {'status': 'success', 'result': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    mode = request.args.get('mode', 'login')
    error = None

    if request.method == 'POST':
        mode = request.form.get('mode')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')

        if mode == 'signup':
            if password != confirm:
                error = "Passwords do not match"
            elif username == "demo" and password == "farm123":
                session['user'] = username
                return redirect(url_for('index'))
            else:
                error = "Only demo account allowed for signup in demo."

        elif mode == 'login':
            if username == "demo" and password == "farm123":
                session['user'] = username
                return redirect(url_for('index'))
            else:
                error = "Invalid credentials. Try demo / farm123"

    return render_template('auth.html', mode=mode, error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth', mode='login'))
@app.before_request
def require_login():
    allowed_routes = ['auth', 'static', 'logout']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect(url_for('auth', mode='login'))


# --------------------------
# Run App
# --------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
