from flask import Flask, render_template, jsonify, request,  send_file,  redirect, url_for
import google.generativeai as genai



app = Flask(__name__)

genai.configure(api_key="AIzaSyAbmCYsZsjfCPf-uakFksDglYasW4EsehE")

# Store locations in memory (as a list of dictionaries)
locations = []

# Route to render HTML template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_message = data['message']
    model = genai.GenerativeModel('gemini-1.5-flash')
    rply = model.generate_content(f"{user_message} your here to give an emergency medical assistance atleast provide some basic assisstance  answer in one or 2 lines without any */ symbols")

    return jsonify({'response': rply.text})


@app.route('/map')
def map():
    return render_template('map.html')

# API endpoint to receive location data from frontend
@app.route('/add_location', methods=['POST'])
def add_location():
    data = request.get_json()
    description = data.get('description')
    lat = data.get('lat')
    lng = data.get('lng')

    if description and lat and lng:
        location = {
            'description': description,
            'lat': lat,
            'lng': lng
        }
        locations.append(location)
        return jsonify({'message': 'Location added successfully!', 'location': location}), 200
    return jsonify({'message': 'Invalid data'}), 400

# API endpoint to get all locations
@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True)
