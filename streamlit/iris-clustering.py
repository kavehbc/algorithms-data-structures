import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import plotly.express as px

def plot(df, features):
    df = df.astype({"Cluster": "category"})
    
    # axis_x = st.selectbox('Axis X',features, index=0)
    # axis_y = st.selectbox('Axis Y',features, index=3)
    # axis_z = st.selectbox('Axis Z',features, index=2)

    axises = st.multiselect('Axis', features, max_selections=3)
    if len(axises) == 3:
        fig = px.scatter_3d(df,
                            x=axises[0],
                            y=axises[1],
                            z=axises[2],
                            color="Cluster",
                            height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Select 3 features.")
        
def kmeans_func(df, features, n_clusters):
    X = df[features]
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
    kmeans.fit(X)
    predicted_clusters = kmeans.predict(X)
    df["Cluster"] = predicted_clusters

    plot(df, features)
        
def dbscan_func(df, features, eps=0.5, min_samples=5):
    X = df[features]
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    predicted_clusters = dbscan.fit_predict(X)
    df["Cluster"] = predicted_clusters
    
    plot(df, features)
    
def load_df():
    # loading iris dataset
    data = load_iris()
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    df["Species"] = data.target
    df["Species_Name"] = df["Species"]

    for index, row in df.iterrows():
        species = int(row["Species"])
        df.loc[index, "Species_Name"] = data.target_names[species]
    
    return df, data.feature_names

def main():
    # loading iris dataset
    df, features = load_df()
    
    st.title("Iris Clustering")
    clustering_method = st.sidebar.selectbox('Clustering Method',
                                             ['K-Means', 'DBSCAN'])
    
    st.sidebar.subheader("Hyperparameters")
    st.header(clustering_method)
    
    if clustering_method == "K-Means":
        n_clusters = st.sidebar.slider("K", min_value=1, max_value=10, value=3, step=1)
        kmeans_func(df=df, features=features, n_clusters=n_clusters)
        
    elif clustering_method == "DBSCAN":
        eps = st.sidebar.number_input("eps", min_value=0.01, max_value=None, value=0.5, step=0.01)
        min_samples = st.sidebar.number_input("Min Samples", min_value=1, max_value=None, value=5, step=1)
        dbscan_func(df=df, features=features, eps=eps, min_samples=min_samples)
        
    
if __name__ == "__main__":
    main()
    