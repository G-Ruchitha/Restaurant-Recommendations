import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse
from collections import defaultdict


def process(user_id):
	# Load the dataset
	data = pd.read_csv("reviews_data.csv")

	# Content-based recommendation
	tfidf_vectorizer = TfidfVectorizer(stop_words='english')
	tfidf_matrix = tfidf_vectorizer.fit_transform(data['Review_Text'].values.astype('U'))
	content_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

	def content_based_recommendation(user_id, content_similarity_matrix, n=5):
	    idx = data[data['User_ID'] == user_id].index[0]
	    sim_scores = list(enumerate(content_similarity_matrix[idx]))
	    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
	    sim_scores = sim_scores[1:n+1]  # Exclude the item itself
	    similar_business_indices = [i[0] for i in sim_scores]
	    similar_business_names = [(data.iloc[idx]['Business_Name'], data.iloc[idx]['Address']) for idx in similar_business_indices]
	    return similar_business_names
	    #return data.iloc[similar_business_indices][['Business_ID', 'Business_Name']]

	reader = Reader(rating_scale=(1, 5))
	def collaborative_filtering_recommendation(user_id, content_similarity_matrix, n=5):
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
	    
		    # Get Business_Name for each Business_ID
		    recommended_businesses = [(data[data['Business_ID'] == business_id]['Business_Name'].iloc[0], 
                                       data[data['Business_ID'] == business_id]['Address'].iloc[0]) 
                                      for business_id, _ in recommendations[:n]]
		    
		    return recommended_businesses
	
		recommendations = get_recommendations(user_id)
		result = [(business_name, address) for business_name, address in recommendations]
		return result    


	# Hybrid recommendation
	def hybrid_recommendation(user_id, content_similarity_matrix, n=5):
	    content_based_rec = content_based_recommendation(user_id, content_similarity_matrix, n)
	    collab_filter_rec = collaborative_filtering_recommendation(user_id, n)
	    hybrid_rec = list(set(content_based_rec) | set(collab_filter_rec))[:n]
	    return(f"{business_name} - {address}" for business_name, address in hybrid_rec)
	    #return data[data['Business_ID'].isin(hybrid_rec)][['Business_ID', 'Business_Name']].drop_duplicates()
	
	hybrid_rec = hybrid_recommendation(user_id, content_similarity, n=5)
	result=hybrid_rec
	return result
#process('HB6EwV37X0R2yuMwwTNfBA')