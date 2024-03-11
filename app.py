from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']
    property_type = request.form.get('property_type', '')
    min_price = request.form.get('min_price', '')
    max_price = request.form.get('max_price', '')
    location = f"{city}, {state} {zip_code}"

    url = "https://us-real-estate-listings.p.rapidapi.com/for-sale"
    querystring = {
        "location": location.strip(),
        "property_type": property_type,
        "price_min": min_price,
        "price_max": max_price,
        "limit": "10"
    }
    headers = {
        "X-RapidAPI-Key": "2e0b32e3admsh9e5edb2fe19207bp1d681djsn63057cdf50a8",
        "X-RapidAPI-Host": "us-real-estate-listings.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        return render_template('results.html', listings=data['listings'])
    else:
        return "Failed to fetch property data. Please try again."

@app.route('/property-details', methods=['GET'])
def property_details():
    property_url = request.args.get('property_url')
    if property_url:
        url = "https://us-real-estate-listings.p.rapidapi.com/propertyPhotos"
        querystring = {"property_url": property_url}
        headers = {
            "X-RapidAPI-Key": "2e0b32e3admsh9e5edb2fe19207bp1d681djsn63057cdf50a8",
            "X-RapidAPI-Host": "us-real-estate-listings.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            photos_data = response.json()
            return render_template('property_details.html', photos=photos_data['photos'])
        else:
            return "Failed to fetch property photos. Please try again."
    return "No property URL provided."

if __name__ == '__main__':
    app.run(debug=True)
