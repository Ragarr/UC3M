import pandas as pd
import numpy as np
from typing import Union
from sklearn.metrics import silhouette_score


class KMeans:
    def __init__(self, n_clusters: int = -2, max_iter: int = 1000, 
                 tolerance: float = 1e-4, random_state: int = None, 
                 verbose: bool = False, init_method: str = 'kmeans++'):
        """KMeans clustering algorithm.

        Args:
            n_clusters (int, optional): Number of clusters, -1 is assigned will search the opt based on elbow method, if -2 based on shiluette. Defaults to -1.
            max_iter (int, optional): Maximum number of iterations. Defaults to 1000.
            tolerance (float, optional): Tolerance for convergence. Defaults to 1e-4.
            random_state (int, optional): Random seed. Defaults to None.
            verbose (bool, optional): Verbosity. Defaults to False.
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.random_state = random_state if random_state else np.random.randint(0, 9999999)
        self.__verbose = verbose
        self.__centroids = None
        self.__inertia = None
        self.__labels = None
        self.__optimal_n_clusters = None
        self.__init_method = init_method
        
    
    @property
    def centroids(self):
        if self.__centroids is None:
            raise ValueError("Model has not been trained yet.")
        return self.__centroids

    @property
    def inertia(self):
        if self.__inertia is None:
            raise ValueError("Model has not been trained yet.")
        return self.__inertia

    @property
    def labels(self):
        if self.__labels is None:
            raise ValueError("Model has not been trained yet.")
        return self.__labels

    @property
    def optimal_n_clusters(self):
        if self.__optimal_n_clusters is None:
            raise ValueError("Optimal number of clusters has not been determined yet.")
        return self.__optimal_n_clusters
    
    
    def __log(self, *args):
        if self.__verbose:
            print(*args)

    def __initialize_centroids(self, X: pd.DataFrame):
        if self.__init_method == 'random':
            np.random.seed(self.random_state)
            # Seleccionar filas aleatorias de X para convertirlo en centroides
            return X.sample(n=self.n_clusters, replace=False, random_state=self.random_state).values
        elif self.__init_method == 'kmeans++':
            return self.__kmeans_plus_plus(pd.DataFrame(X))
        else:
            raise ValueError(f"Invalid initialization method: {self.__init_method}")

    def __kmeans_plus_plus(self, X: pd.DataFrame) -> np.ndarray:
        np.random.seed(self.random_state)
        centroids = np.zeros((self.n_clusters, X.shape[1]))
        # Seleccionar el primer centroide aleatoriamente
        centroids[0] = X.sample(1, random_state=self.random_state).values[0]

        for k in range(1, self.n_clusters):
            # Calcular la distancia de cada punto al centroide más cercano
            distances = np.linalg.norm(X.values[:, np.newaxis] - centroids[:k], axis=2)
            # Seleccionar la distancia más corta
            distances = np.min(distances, axis=1)
            # Normalizar las distancias para obtener probabilidades de selección 
            probabilities = np.zeros(X.shape[0])
            probabilities += distances ** 2
            probabilities /= np.sum(probabilities)
            # Seleccionar el siguiente centroide con probabilidad proporcional a la distancia
            centroids[k] = X.sample(1, weights=probabilities, random_state=self.random_state).values[0]

        return centroids


    def __compute_distances(self, X: pd.DataFrame, centroids: np.ndarray) -> np.ndarray:
        # Calcular la distancia de cada punto a cada centroide
        distances = np.zeros((X.shape[0], self.n_clusters))
        for k in range(self.n_clusters):
            # Calcular la distancia euclidiana de cada punto al centroide k
            distances[:, k] = np.linalg.norm(X.values - centroids[k], axis=1)
        return distances

    def __update_centroids(self, X: pd.DataFrame, labels: np.ndarray) -> np.ndarray:
        # Calcular el nuevo centroide como la media de los puntos asignados a cada cluster
        centroids = np.zeros((self.n_clusters, X.shape[1]))
        for k in range(self.n_clusters):
            # Calcular la media de los puntos asignados al cluster k
            centroids[k] = X[labels == k].mean(axis=0)
        return centroids

    def __compute_inertia(self, X: pd.DataFrame, labels: np.ndarray, centroids: np.ndarray) -> float:
        # Calcular la inercia como la suma de las distancias al cuadrado de cada punto a su centroide
        distances = self.__compute_distances(X, centroids)
        return np.sum(distances[np.arange(X.shape[0]), labels])

    def find_optimal_n_clusters_elbow(self, X: Union[pd.DataFrame, np.ndarray], n_clusters_range: range = range(2, 11)):
        
        #  Si X es un DataFrame, convertirlo a un ndarray
        if isinstance(X, pd.DataFrame):
            X = X.values

        # Calcular la inercia para cada número de clusters en el rango
        inertias = []
        for n_clusters in n_clusters_range:
            # Entrenar el modelo con n_clusterS
            kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state)
            kmeans.fit(X)
            # Guardar la inercia
            inertias.append(kmeans.inertia)

        # Calcular la diferencia de inercias entre cada par de clusters
        dists = [inertias[i + 1] - inertias[i] for i in range(len(inertias) - 1)]
        
        # Encontrar el codo en la curva de inercias
        elbow_index = np.argmax(dists)
        optimal_n_clusters = n_clusters_range[elbow_index + 1]
        self.__log(f"Optimal number of clusters: {optimal_n_clusters}")

        self.__optimal_n_clusters = optimal_n_clusters
        return optimal_n_clusters
    
    def find_optimal_n_clusters_silhouette(self, X: Union[pd.DataFrame, np.ndarray], n_clusters_range: range = range(2, 11)):
        #  Si X es un DataFrame, convertirlo a un ndarray
        if isinstance(X, pd.DataFrame):
            X = X.values

        # Calcular el coeficiente de silueta para cada número de clusters en el rango
        silhouettes = []
        for n_clusters in n_clusters_range:
            # Entrenar el modelo con n_clusterS
            kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state)
            kmeans.fit(X)
            # Calcular el coeficiente de silueta
            silhouette = silhouette_score(X, kmeans.labels)
            # Guardar el coeficiente de silueta
            silhouettes.append(silhouette)

        # Encontrar el número de clusters con el coeficiente de silueta más alto
        optimal_n_clusters = n_clusters_range[np.argmax(silhouettes)]
        self.__log(f"Optimal number of clusters: {optimal_n_clusters}")

        self.__optimal_n_clusters = optimal_n_clusters
        return optimal_n_clusters
    
    def fit(self, X: Union[pd.DataFrame, np.ndarray]):
        
        # Si n_clusters es -1, buscar el número óptimo de clusters
        if self.n_clusters == -1:
            self.n_clusters = self.find_optimal_n_clusters_elbow(X)
        
        if self.n_clusters == -2:
            self.n_clusters = self.find_optimal_n_clusters_silhouette(X)
            
        # Convertir a numpy array
        if isinstance(X, pd.DataFrame):
            X = X.values

        # Inicializar los centroides
        centroids = self.__initialize_centroids(pd.DataFrame(X))
        prev_centroids = centroids.copy()
        for _ in range(self.max_iter):
            # Asignar cada punto al cluster más cercano
            distances = self.__compute_distances(pd.DataFrame(X), centroids)
            labels = np.argmin(distances, axis=1)
            # Actualizar los centroides con la media de los puntos asignados a cada cluster
            centroids = self.__update_centroids(pd.DataFrame(X), labels)
            self.__inertia = self.__compute_inertia(pd.DataFrame(X), labels, centroids)
            self.__log(f"Iteration {_ + 1}: inertia = {self.__inertia}")
            if np.linalg.norm(centroids - prev_centroids) < self.tolerance:
                self.__log(f"Convergence reached after {_+1} iterations.")
                break
            prev_centroids = centroids.copy()

        self.__centroids = centroids
        self.__labels = labels


    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        if self.__centroids is None:
            raise ValueError("Model has not been trained yet.")
        # convertir a numpy array
        if isinstance(X, pd.DataFrame):
            X = X.values
        # Calcular la distancia de cada punto a cada centroide
        distances = self.__compute_distances(pd.DataFrame(X), self.__centroids)
        # Asignar cada punto al cluster más cercano y devolver los labels
        return np.argmin(distances, axis=1)

    def fit_predict(self, X: Union[pd.DataFrame, np.ndarray]):
        self.fit(X)
        return self.predict(X)
    
    def __str__(self):
        return f"KMeans(n_clusters={self.n_clusters}, max_iter={self.max_iter}, tolerance={self.tolerance}, random_state={self.random_state})"  
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return self.n_clusters
    
    


if __name__ == "__main__":
    from sklearn.datasets import make_blobs
    from sklearn import cluster

    X, y = make_blobs(n_samples=1000, centers=3, n_features=2, random_state=42)
    kmeans = KMeans(n_clusters=-2, random_state=42)
    kmeans.fit(X)
    
    print("Centroids:")
    print(kmeans.centroids)