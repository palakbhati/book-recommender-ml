import streamlit as st
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

st.set_page_config(page_title="Book Recommender", layout="wide")

st.title("📚 Book Recommendation System")

# ---------- Popular Books Section ----------
st.header("🔥 Popular Books")

cols = st.columns(5)

for i in range(5):
    with cols[i]:
        st.image(popular_df['Image-URL-M'].values[i])
        st.markdown(f"**{popular_df['Book-Title'].values[i]}**")
        st.text(popular_df['Book-Author'].values[i])
        st.text(f"⭐ {popular_df['avg_ratings'].values[i]}")
        st.text(f"🗳 {popular_df['num_ratings'].values[i]}")

st.divider()

# ---------- Recommendation Section ----------
st.header("🔍 Recommend Books")

book_list = pt.index.values
selected_book = st.selectbox("Select a book", book_list)

if st.button("Recommend"):
    try:
        index = np.where(pt.index == selected_book)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:5]

        st.subheader("📖 Recommended Books")

        cols = st.columns(4)

        for col, i in zip(cols, similar_items):
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            temp_df = temp_df.drop_duplicates('Book-Title')

            with col:
                st.image(temp_df['Image-URL-M'].values[0])
                st.markdown(f"**{temp_df['Book-Title'].values[0]}**")
                st.text(temp_df['Book-Author'].values[0])

    except IndexError:
        st.error("Book not found in database.")
 