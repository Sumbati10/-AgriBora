

from flask import Flask, render_template, request, send_from_directory
import random, os
from werkzeug.utils import secure_filename
from functions import img_predict, get_diseases_classes, get_crop_recommendation, get_fertilizer_recommendation, soil_types, Crop_types, crop_list


app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/crop-recommendation', methods=['GET', 'POST'])
def crop_recommendation():
	if request.method == "POST":
		to_predict_list = request.form.to_dict()
		to_predict_list = list(to_predict_list.values())
		to_predict_list = list(map(float, to_predict_list))
		result = get_crop_recommendation(to_predict_list)
		return render_template("recommend_result.html", result=result)
	else:
		return render_template('crop-recommend.html')

@app.route('/fertilizer-recommendation', methods=['GET', 'POST'])
def fertilizer_recommendation():
	if request.method == "POST":
		to_predict_list = request.form.to_dict()
		to_predict_list = list(to_predict_list.values())
		to_predict_list = list(map(float, to_predict_list))
		result = get_fertilizer_recommendation(
			num_features=to_predict_list[:-2],
			cat_features=to_predict_list[-2:]
		)
		return render_template("fertilizer-recommend.html", result=result)
	else:
		return render_template(
			'fertilizer-recommend.html', 
			soil_types=enumerate(soil_types),
			crop_types=enumerate(Crop_types)
		)

	
@app.route('/crop-disease', methods=['POST','GET'])
def find_crop_disease():
	if request.method=="GET":
		return render_template('crop-disease.html', crops=crop_list)
	else:
		file = request.files["file"]
		crop = request.form["crop"]

		basepath = os.path.dirname(__file__)
		file_path = os.path.join(basepath,'uploads',  secure_filename(file.filename))
		file.save(file_path)
		prediction = img_predict(file_path, crop)
		result = get_diseases_classes(crop, prediction)

		return render_template('disease-prediction-result.html', image_file_name=file.filename, result=result)
	
import requests

@app.route('/weather', methods=['GET', 'POST'])
def weather():
	if request.method == 'POST':
		city = request.form['city']
		api_key = "96cd3e85fd1aa5bbbfc318b428373d8b"
		base_url = "https://api.openweathermap.org/data/2.5/weather"

		params = {
			'q': city,
			'appid': api_key,
			'units': 'metric'  # to get °C
		}

		response = requests.get(base_url, params=params)
		data = response.json()

		if data.get('cod') != 200:
			error_msg = data.get("message", "City not found.")
			return render_template('weather.html', error=error_msg)

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
            else:
                # Save user logic (to database or file) here
                return redirect(url_for('auth', mode='login'))

        elif mode == 'login':
            # Validate user logic here
            return redirect(url_for('index'))

    return render_template('auth.html', mode=mode, error=error)



if __name__ == '__main__':
	port=int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port,debug=True)