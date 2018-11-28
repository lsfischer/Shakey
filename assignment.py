import pandas as pd
import numpy as np
from helper_functions import *
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score

class Assignment:
    """
        Class responsable for the core implementation of the assignmet

        Params:
            filename - Name of the data file to read
    """


    EARTH_RADIUS = 6371 #Earth radius in km


    def __init__(self, filename):
        """
            Initializer for the Assignment class.
            Obtains the data from a given file and shuffles that data.

            Params:
                filename - name of the file to obtain the data from
        """

        self.data = pd.read_csv(filename).loc[:, ["latitude", "longitude", "fault"]] #read and select select just latitude longitude and fault

        #Converting coordinates to Earth-centered, Earth-fixed (x, y, z)
        self.data["x"] = self.EARTH_RADIUS * np.cos(self.data["latitude"] * (np.pi/180.0)) * np.cos(self.data["longitude"] * (np.pi/180.0))
        self.data["y"] = self.EARTH_RADIUS * np.cos(self.data["latitude"] * (np.pi/180.0)) * np.sin(self.data["longitude"] * (np.pi/180.0))
        self.data["z"] = self.EARTH_RADIUS * np.sin(self.data["latitude"] * (np.pi/180.0))
        #plot_3D(self.data["x"],self.data["y"],self.data["z"])
        # plot_classes(self.data["fault"], self.data["longitude"], self.data["latitude"])


    def k_means(self, k):
        coords = self.data[["x", "y", "z"]].values
        kmeans = KMeans(n_clusters = k).fit(coords)
        labels = kmeans.predict(coords)
        centroids = kmeans.cluster_centers_
        print(silhouette_score(coords, labels))
        print(rand_index(self.data["fault"].values, labels))
        plot_3D_with_centroids(self.data["x"],self.data["y"],self.data["z"], centroids[:, 0], centroids[:, 1], centroids[:, 2])


    def gaussian_mix(self, num_components):
        coords = self.data[["x", "y", "z"]].values
        gmm = GaussianMixture(n_components =  num_components).fit(coords)
        labels = gmm.predict(coords)
        print(silhouette_score(coords, labels))
        print(rand_index(self.data["fault"].values, labels))
        #o gmm.predict_proba(coords) da-nos o grau de pertenca de cada ponto as diferentes gaussianas


    def dbscan(self):
        coords = self.data[["x", "y", "z"]].values
        estimated_epsilon = select_epsilon(coords)
        dbscan = DBSCAN(eps = estimated_epsilon, min_samples = 4).fit(coords)
        labels = dbscan.labels_
        print(silhouette_score(coords, labels))
        print(rand_index(self.data["fault"].values, labels))



#Maybe identify where they're more dense with DBSCAN varying number of neighbours (how many sisms ocour near eachother to be relevant), value of epislon (the distance the sisms have to be to each other to be relevant)

# TODO
#     - Find a way to choose K in k k means
#     - Find a way to choose the number of components in gaussian mixture model
#     - Implement Graphics
#     - Ter plots dos params vs scores
#     - Para o Kmeans secalhar o vector quantization
#     - Para o DBSCAN buscar os pontos de maior densidade de sismos
#     - Se calhar usar o GMM para ir buscar "interseções" entre faults, ou zonas que sejam "influenciadas" por varias faults (que é a area da gaussiana)