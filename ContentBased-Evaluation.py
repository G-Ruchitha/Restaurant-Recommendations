import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def process(user_id):
    # Load the dataset
    data = pd.read_csv("reviews_data.csv")

    # Preprocess the text data
    data['Review_Text'] = data['Review_Text'].fillna('')  # Replace NaN values with empty string

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['Review_Text'])

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Function to get recommendations based on a given user ID
    def get_recommendations(user_id, cosine_sim=cosine_sim):
        if user_id not in data['User_ID'].values:
            print("User ID not found in the dataset.")
            return pd.DataFrame(), []

        idx = data[data['User_ID'] == user_id].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        business_indices = [i[0] for i in sim_scores]
        recommended_businesses = data.iloc[business_indices]
        
        # Get the corresponding ratings for recommended businesses
        recommended_ratings = data.iloc[business_indices]['Rating'].tolist()
        
        # Return both recommended businesses and their ratings
        return recommended_businesses, recommended_ratings

    # Get recommendations and ratings for the given user ID
    recommendations, predicted_ratings = get_recommendations(user_id)
    print(recommendations)
    result = recommendations['Business_Name'].tolist()
    print("Recommended businesses:", result)
    
    # Calculate MAE and MSE if 'Rating' column is available
    if 'Rating' in data.columns:
        actual_ratings = data[data['User_ID'] == user_id]['Rating'].values
        print("actual_ratings",actual_ratings)
        print("predicted_ratings",predicted_ratings)
        predicted_ratings=[predicted_ratings[0]]
        print("predicted_ratings0",predicted_ratings)
        mae = mean_absolute_error([actual_ratings[5]], predicted_ratings)
        mse = mean_squared_error([actual_ratings[5]], predicted_ratings)
        
        print("MAE error metric value for Content based filtering is :", mae)
        print("MSE error metric value for Content based filtering is :", mse)
    else:
        print("Rating information not available. Cannot calculate MAE and MSE.")

    return result


process("MMgdhI98OwqxegvHQWhbNg")
