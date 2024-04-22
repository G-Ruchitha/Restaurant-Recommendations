from surprise import accuracy
import pandas as pd
from surprise import Dataset, Reader, KNNBasic, accuracy
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

    # Evaluate the model
    predictions = model.test(testset)
    #rmse = accuracy.rmse(predictions)
    mse = accuracy.mse(predictions)
    mae = accuracy.mae(predictions)
    #print(mse)
    #print(f"RMSE: {rmse}, MAE: {mae}")
    print("MAE error metric value for Collaborative based filtering is :", mae)
    print("MSE error metric value for Collaborative based filtering is :", mse)


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
        
        # Get Business_Name for each Business_ID
        recommended_businesses = [(data[data['Business_ID'] == business_id]['Business_Name'].iloc[0], business_id) for business_id, _ in recommendations[:n]]
        
        return recommended_businesses

    # Call get_recommendations and return its result
    recommendations = get_recommendations(user_id)
    result=[]
    for business_name, business_id in recommendations:
        result.append(business_name)
    return result

# Call the process function with the user_id
print(process("MMgdhI98OwqxegvHQWhbNg"))
