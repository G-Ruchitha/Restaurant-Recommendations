from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
import pandas as pd


def process(user_id):
    # Load the dataset
    data = pd.read_csv("reviews_data.csv")

    # Define a reader
    reader = Reader(rating_scale=(1, 5))

    # Load the dataset into Surprise's format
    surprise_data = Dataset.load_from_df(data[['User_ID', 'Business_ID', 'Rating']], reader)

    # Split the data into train and test sets
    trainset, testset = train_test_split(surprise_data, test_size=0.2, random_state=42)

    # Define and train the collaborative filtering model
    sim_options = {'name': 'cosine', 'user_based': True}  # Use user-based collaborative filtering with cosine similarity
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)

    # Get recommendations for a given user
    def get_recommendations(user_id, n=5):
        # Get the list of businesses the user has not rated
        rated_businesses = data[data['User_ID'] == user_id]['Business_ID']
        all_businesses = data['Business_ID'].unique()
        unrated_businesses = list(set(all_businesses) - set(rated_businesses))

        # Predict ratings for unrated businesses
        recommendations = []
        for business_id in unrated_businesses:
            predicted_rating = model.predict(user_id, business_id).est
            recommendations.append((business_id, predicted_rating))

        # Sort recommendations by predicted rating and return top n
        recommendations.sort(key=lambda x: x[1], reverse=True)
    
        # Get Business_Name and Address for each Business_ID
        recommended_businesses = [(data[data['Business_ID'] == business_id]['Business_Name'].iloc[0], 
                                   data[data['Business_ID'] == business_id]['Address'].iloc[0]) 
                                  for business_id, _ in recommendations[:n]]
        
        return recommended_businesses

    recommendations = get_recommendations(user_id)
    result = ["{} - {}".format(business_name, address) for business_name, address in recommendations]
    return result

# Test the function
# process("SKejKH6BmHG8sL6fs9PeMg")
