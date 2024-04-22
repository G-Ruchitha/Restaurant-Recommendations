import pandas as pd

# Read the original CSV file
df = pd.read_csv("reviews_data.csv")

# Convert "User" column to numerical values
df['USER_ID'] = df['User_ID'].astype('category').cat.codes

# Step 1: Extract Business_ID column
business_ids = df["Business_ID"]

# Step 2: Read yelp_results.csv and extract Business_ID and Name columns
yelp_df = pd.read_csv("yelp_results.csv")
yelp_df = yelp_df[["ID", "Name"]]

# Step 3: Merge the two dataframes based on Business_ID
merged_df = pd.merge(df, yelp_df, left_on="Business_ID", right_on="ID", how="left")

# Step 4: Add the Name column to the original DataFrame
df["Business_Name"] = merged_df["Name"]

# Step 5: Write the updated dataframe to a new CSV file
df.to_csv("review2_with_names.csv", index=False)
