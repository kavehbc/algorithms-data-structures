import streamlit as st

def main():
    st.title("Iris Clustering")
    clustering_method = st.sidebar.selectbox('Clustering Method',
                                             ['K-Means', 'DBSCAN'])
    
    st.sidebar.subheader("Hyperparameters")
    
    if clustering_method == "K-Means":
        k = st.sidebar.slider("K", min_value=1, max_value=10, value=3, step=1)
    elif clustering_method == "DBSCAN":
        eps = st.sidebar.number_input("eps", min_value=0.01, max_value=None, value=0.5, step=0.01)
        min_samples = st.sidebar.number_input("Min Samples", min_value=1, max_value=None, value=5, step=1)
    
if __name__ == "__main__":
    main()
    