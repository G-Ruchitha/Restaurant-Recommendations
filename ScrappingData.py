import requests
import csv




def search_businesses(location, term='restaurant', limit=10):
    # Yelp Fusion API endpoint for business search
    endpoint = 'https://api.yelp.com/v3/businesses/search'
    
    # Replace 'YOUR_API_KEY' with your actual Yelp API key
    API_KEY = '3G-5GLC3PMUHx-1L0zlfNum72_QfIDju7C30ZPrTAN422iIb4LAG5SLPiPx6-ctqPJQXxStEvDt6auX3tmrAFNLVtxSIm8oTPXA0-pbMaEUbjQOiQWrGTC6mvNPAZXYx'


    # Set up headers with the API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Set up parameters for the search
    params = {
        'location': location,
        'term': term,
        'limit': limit
    }

    # Make the API request
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        # Parse and return the JSON response
        return response.json()
    else:
        # Print an error message if the request was unsuccessful
        print(f"Error: {response.status_code}")
        return None

def write_to_csv(businesses, filename='ScrappingData/yelp_results.csv'):
    # Write business data to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['ID', 'Name', 'Alias', 'Rating', 'Review Count', 'Address', 'Phone', 'Categories']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data for each business
        for business in businesses:
            writer.writerow({
                'ID': business['id'],
                'Name': business['name'],
                'Alias': business['alias'],
                'Rating': business['rating'],
                'Review Count': business['review_count'],
                'Address': ', '.join(business['location']['display_address']),
                'Phone': business.get('phone', 'N/A'),
                'Categories': ', '.join([category['title'] for category in business['categories']])
            })



def processBusiness(location):
	#location = 'New York'
	result = search_businesses(location)
	
	# Write data to CSV file
	if result:
		businesses = result.get('businesses', [])
		write_to_csv(businesses)
	else:
		print("No results found.")
	

def processReview():
	# API endpoint and parameters
	url_base = "https://api.yelp.com/v3/businesses/"
	reviews_endpoint = "/reviews?limit=20&sort_by=yelp_sort"
	
	# Replace 'YOUR_API_KEY' with your actual Yelp API key
	api_key = '3G-5GLC3PMUHx-1L0zlfNum72_QfIDju7C30ZPrTAN422iIb4LAG5SLPiPx6-ctqPJQXxStEvDt6auX3tmrAFNLVtxSIm8oTPXA0-pbMaEUbjQOiQWrGTC6mvNPAZXYx'


	# Headers with API key
	headers = {
	    "accept": "application/json",
	    "Authorization": f"Bearer {api_key}"
	}

	# Open the CSV file containing business data
	with open("ScrappingData/yelp_results.csv", mode="r", newline="", encoding="utf-8") as csv_file:
	    csv_reader = csv.DictReader(csv_file)

	    # Open a new CSV file for writing reviews data
	    with open("ScrappingData/reviews_data.csv", mode="w", newline="", encoding="utf-8") as reviews_csv_file:
	        fieldnames = ["Business_ID","Business_Name", "User_ID", "Reviewer_Name", "Review_Text", "Rating", "Time_Created"]
	        csv_writer = csv.DictWriter(reviews_csv_file, fieldnames=fieldnames)

	        # Write header
	        csv_writer.writeheader()

	        # Iterate through each row in the CSV file
	        for row in csv_reader:
	            business_id = row["ID"]
	            print(business_id)
	            business_name=row["Name"]
	            print(business_name)
     
	            # Construct the complete URL
	            full_url = url_base + business_id + reviews_endpoint
	
	            # Make the API request
	            response = requests.get(full_url, headers=headers)
	
	            # Check if the request was successful (status code 200)
	            if response.status_code == 200:
	                reviews_data = response.json().get("reviews", [])

	                # Iterate through each review
	                for review in reviews_data:
	                    csv_writer.writerow({
	                        "Business_ID": business_id,
	                        "Business_Name": business_name,
	                        "User_ID": review["id"],
	                        "Reviewer_Name": review["user"]["name"],
	                        "Review_Text": review["text"],
	                        "Rating": review["rating"],
	                        "Time_Created": review["time_created"]
	                    })
	             
                    
	            else:
	                print(f"Failed to retrieve reviews for Business ID {business_id}. Status code: {response.status_code}")
#process()