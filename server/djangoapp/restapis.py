import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, CarMake, CarModel, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if api_key:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', api_key),
                                        params=kwargs)
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, json=json_payload)
    except:
        # If any error occurs        
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc['state'])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            review_doc = review
            print(review_doc)
            # Create a CarDealer object with values in `doc` object
            purchase_date = review_doc["purchase_date"] if "purchase_date" in review_doc else '1970-01-01'
            car_make = review_doc["car_make"] if "car_make" in review_doc else 'NA'
            car_model = review_doc["car_model"] if "car_model" in review_doc else 'NA'
            car_year = review_doc["car_year"] if "car_year" in review_doc else 1979
            sentiment = analyze_review_sentiments(review_doc['review'])
            print(sentiment)
            review_obj = DealerReview(id=review_doc["id"], name=review_doc["name"],
                                   dealership=review_doc["dealership"], review=review_doc["review"], 
                                   purchase=review_doc["purchase"],
                                   purchase_date=purchase_date,
                                   car_make=car_make, 
                                   car_model=car_model, 
                                   car_year=car_year,
                                   sentiment=sentiment)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    """
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/56571563-69dc-42a1-be00-f8358659585c/v1/analyze?version=2019-07-12'
    api_key= '8F95_SowNELZg2RrQBm3BuwZf3R0TVdFW3-qDxctbJte'
    params = dict()
    print(text)
    params["text"] = text  
    params["features"] = {
        "sentiment": { "targets": ["apples", "oranges", "broccoli"] },
        "keywords": {
        "emotion": True
        }
    }  
    response = requests.post(url, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', api_key), data=params)
    print(response)
    """
    authenticator = IAMAuthenticator('8F95_SowNELZg2RrQBm3BuwZf3R0TVdFW3-qDxctbJte')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/56571563-69dc-42a1-be00-f8358659585c')
    try:
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions())).get_result()

        print(json.dumps(response, indent=2))
        return response['sentiment']['docuemnt']['label']
    except:
        return 'neutral'



