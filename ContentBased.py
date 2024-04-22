import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


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

    # Function to get recommendations based on a given business ID
    def get_recommendations(user_id, cosine_sim=cosine_sim):
        if user_id not in data['User_ID'].values:
            print("User ID not found in the dataset.")
            return []  # Return an empty list if user_id is not found

        idx = data[data['User_ID'] == user_id].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:]  # Remove the first element, which is the user itself
        business_indices = [i[0] for i in sim_scores]

        recommendations = []
        for idx in business_indices:
            business_name = data.iloc[idx]['Business_Name']
            business_address = data.iloc[idx]['Address']
            business_info = f"{business_name} - {business_address}"
            if (business_info) not in recommendations:
                recommendations.append((business_info))
            if len(recommendations) == 5:  # Break when you have 5 unique recommendations
                break

        return recommendations

    recommendations = get_recommendations(user_id)
    for business_info in recommendations:
        print(business_info)
    return recommendations


# Test the function
process("HB6EwV37X0R2yuMwwTNfBA")
