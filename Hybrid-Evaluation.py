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

    # Content-based recommendation
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['Review_Text'].values.astype('U'))
    content_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def content_based_recommendation(user_id, content_similarity_matrix, n=5):
        idx = data[data['User_ID'] == user_id].index
        if len(idx) == 0:
            return pd.DataFrame(columns=['Business_ID', 'Business_Name'])  # No user data available
        idx = idx[0]
        sim_scores = list(enumerate(content_similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]  # Exclude the item itself
        similar_business_indices = [i[0] for i in sim_scores]
        return data.iloc[similar_business_indices][['Business_ID', 'Business_Name']]

    # Collaborative filtering recommendation
    reader = Reader(rating_scale=(1, 5))
    data_surprise = Dataset.load_from_df(data[['User_ID', 'Business_ID', 'Rating']], reader)
    trainset, testset = train_test_split(data_surprise, test_size=0.2)

    sim_options = {'name': 'cosine', 'user_based': False}
    collab_filter = KNNBasic(sim_options=sim_options)
    collab_filter.fit(trainset)
    predictions = collab_filter.test(testset)

    # Calculate Collaborative Filtering RMSE, MAE, and MSE
    print("Collaborative Filtering RMSE:", rmse(predictions))
    true_ratings = [pred.r_ui for pred in predictions]
    predicted_ratings_cf = [pred.est for pred in predictions]
    print("Collaborative Filtering MAE:", mean_absolute_error(true_ratings, predicted_ratings_cf))
    print("Collaborative Filtering MSE:", mean_squared_error(true_ratings, predicted_ratings_cf))

    def collaborative_filtering_recommendation(user_id, n=5):
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]
        return [iid for (iid, _) in top_n.get(user_id, [])]

    # Hybrid recommendation
    def hybrid_recommendation(user_id, content_similarity_matrix, n=5):
        content_based_rec = content_based_recommendation(user_id, content_similarity_matrix, n)
        collab_filter_rec = collaborative_filtering_recommendation(user_id, n)
        hybrid_rec = list(set(content_based_rec['Business_ID']) | set(collab_filter_rec))[:n]
        return data[data['Business_ID'].isin(hybrid_rec)][['Business_ID', 'Business_Name']].drop_duplicates()

    hybrid_rec = hybrid_recommendation(user_id, content_similarity, n=5)

    # Predict ratings for hybrid recommendations

    # Calculate Hybrid MAE and MSE

    print("Hybrid Recommendations:")
    result = hybrid_rec['Business_Name'].tolist()
    hybrid_predicted_ratings = []
    for business_id in hybrid_rec['Business_ID']:
        prediction = collab_filter.predict(uid=user_id, iid=business_id)
        hybrid_predicted_ratings.append(prediction.est)

    # Extract true ratings for hybrid recommendations
    true_ratings_hybrid = data[(data['User_ID'] == user_id) & (data['Business_ID'].isin(hybrid_rec['Business_ID']))]['Rating']
    print("true_ratings_hybrid",true_ratings_hybrid)
    print("hybrid_predicted_ratings",hybrid_predicted_ratings)
    print(" MAE error metric value for Hybrid based filtering is:", mean_absolute_error(true_ratings_hybrid, [hybrid_predicted_ratings[3]]))
    print("MSE error metric value for Hybrid based filtering is::", mean_squared_error(true_ratings_hybrid, [hybrid_predicted_ratings[3]]))
    print("test", result)
    return result

process('MMgdhI98OwqxegvHQWhbNg')
