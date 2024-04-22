import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse
from collections import defaultdict
from sklearn.metrics import mean_absolute_error, mean_squared_error


def process(user_id):
	# Load the dataset
	data = pd.read_csv("reviews_data.csv")
	reader = Reader(rating_scale=(1, 5))
	data_surprise = Dataset.load_from_df(data[['User_ID', 'Business_ID', 'Rating']], reader)
	trainset, testset = train_test_split(data_surprise, test_size=0.2)
	sim_options = {'name': 'cosine', 'user_based': False}
	model = KNNBasic(sim_options=sim_options)
	model.fit(trainset)
	
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
	    similar_business_names = data.iloc[similar_business_indices]['Business_Name'].tolist()
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
		    recommended_businesses = [(data[data['Business_ID'] == business_id]['Business_Name'].iloc[0], business_id) for business_id, _ in recommendations[:n]]
		    
		    return recommended_businesses
	
		recommendations = get_recommendations(user_id)
		result=[]
		for business_name, business_id in recommendations:
			result.append(business_name)
			print(result)
		return result    


	# Hybrid recommendation
	def hybrid_recommendation(user_id, content_similarity_matrix, n=5):
	    content_based_rec = content_based_recommendation(user_id, content_similarity_matrix, n)
	    print("content_based_rec" ,content_based_rec )
	    collab_filter_rec = collaborative_filtering_recommendation(user_id, n)
	    print("collab_filter_rec ",collab_filter_rec )
	    hybrid_rec = list(set(content_based_rec) | set(collab_filter_rec))[:n]
	    print("hybrid_rec ",hybrid_rec )
	    return(hybrid_rec )
	    #return data[data['Business_ID'].isin(hybrid_rec)][['Business_ID', 'Business_Name']].drop_duplicates()
	
	hybrid_rec = hybrid_recommendation(user_id, content_similarity, n=5)
	print("Hybrid Recommendations:")
	result=hybrid_rec
	
	
	hybrid_predicted_ratings = []
	for business_name in hybrid_rec:
		prediction = model.predict(uid=user_id, iid=business_name)
		hybrid_predicted_ratings.append(prediction.est)
		rounded_hybrid_predicted_ratings = [round(pred) for pred in hybrid_predicted_ratings]

	#true_ratings_hybrid = data[(data['User_ID'] == user_id) & (data['Business_Name'].isin(hybrid_rec['Business_Name']))]['Rating']
	true_ratings_hybrid = data[data['Business_Name'].isin(hybrid_rec)]['Rating'].tolist()
	true_ratings_hybrid= true_ratings_hybrid[:5]

	print("Hybrid MAE:", mean_absolute_error(true_ratings_hybrid,rounded_hybrid_predicted_ratings ))
	print("Hybrid MSE:", mean_squared_error(true_ratings_hybrid, rounded_hybrid_predicted_ratings))
	print("Hybrid",result)
	return result
process('MMgdhI98OwqxegvHQWhbNg')