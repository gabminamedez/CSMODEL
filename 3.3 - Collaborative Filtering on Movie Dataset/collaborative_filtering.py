import numpy as np
import pandas as pd

class CollaborativeFiltering(object):

    def __init__(self, k):
        """Class constructor for KMeans
        Arguments:
            k {int} -- number of similar items to consider
        """
        self.k = k

    def get_row_mean(self, data):
        """Returns the mean of each row in the DataFrame or the mean of the
        Series. If the parameter data is a DataFrame, the function will
        return a Series containing the mean of each row in the DataFrame. If
        the parameter data is a Series, the function will return a np.float64
        which is the mean of the Series. This function should not consider
        blank ratings represented as NaN.

        Arguments:
            data {DataFrame or Series} -- dataset
        Returns:
            Series or np.float64 --
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Check if the parameter data is a Series or a DataFrame

        # TODO: return the mean of each row if the parameter data is a
        # DataFrame. Return the mean of the Series if the parameter data is a
        # Series.
        # Hint: Use pandas.DataFrame.mean() or pandas.Series.mean() functions.
        if isinstance(data, pd.DataFrame):
            return data.mean(axis=1)

        elif isinstance(data, pd.Series):
            return data.mean()

    def normalize_data(self, data, row_mean):
        """Returns the data normalized by subtracting the row mean.

        For the arguments point1 and point2, you can only pass these
        combinations of data types:
        - DataFrame and Series -- returns DataFrame
        - Series and np.float64 -- returns Series

        For a DataFrame and a Series, if the shape of the DataFrame is
        (3, 2), the shape of the Series should be (3,) to enable broadcasting.
        This operation will result to a DataFrame of shape (3, 2)

        Arguments:
            data {DataFrame or Series} -- dataset
            row_mean {Series or np.float64} -- mean of each row
        Returns:
            DataFrame or Series -- normalized data
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Check if the combination of parameters is correct
        # Normalize the parameter data by parameter row_mean.
        # HINT: Use pandas.DataFrame.subtract() or pandas.Series.subtract()
        # functions.
        if isinstance(data, pd.DataFrame) and isinstance(row_mean, pd.Series):
            return data.subtract(row_mean, axis=0)

        elif isinstance(data, pd.Series):
            return data.subtract(row_mean)

    def get_cosine_similarity(self, vector1, vector2):
        """Returns the cosine similarity between two vectors. These vectors can
        be represented as 2 Series objects. This function can also compute the
        cosine similarity between a list of vectors (represented as a
        DataFrame) and a single vector (represented as a Series), using
        broadcasting.

        For the arguments vector1 and vector2, you can only pass these
        combinations of data types:
        - Series and Series -- returns np.float64
        - DataFrame and Series -- returns pd.Series

        For a DataFrame and a Series, if the shape of the DataFrame is
        (3, 2), the shape of the Series should be (2,) to enable broadcasting.
        This operation will result to a Series of shape (3,)

        Arguments:
            vector1 {Series or DataFrame} - vector
            vector2 {Series or DataFrame} - vector
        Returns:
            np.float64 or pd.Series -- contains the cosine similarity between
            two vectors
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Check if the parameter data is a Series or a DataFrame

        # TODO: Compute the cosine similarity between the two parameters.
        # HINT: Use np.sqrt() and pandas.DataFrame.sum() and/or
        # pandas.Series.sum() functions.
        if isinstance(vector1, pd.Series) and isinstance(vector2, pd.Series):
            vector1a = vector1.apply(lambda x: x * x)
            vector2a = vector2.apply(lambda x: x * x)

            return (np.sum(vector1.multiply(vector2))) / (np.sqrt(vector1a.sum()) * np.sqrt(vector2a.sum()))

        elif isinstance(vector1, pd.DataFrame) and isinstance(vector2, pd.Series):
            vector2a = vector2.apply(lambda x: x * x)
            sims = []
            idxs = []

            for i, row in vector1.iterrows():
                rowa = row.apply(lambda x: x * x)
                idxs.append(i)
                sims.append((np.sum(row.multiply(vector2))) / (np.sqrt(rowa.sum()) * np.sqrt(vector2a.sum())))

            return pd.Series(sims, idxs)

        elif isinstance(vector1, pd.Series) and isinstance(vector2, pd.DataFrame): 
            vector1a = vector1.apply(lambda x: x * x)
            sims = []
            idxs = []

            for i, row in vector2.iterrows():
                rowa = row.apply(lambda x: x * x)
                idxs.append(i)
                sims.append((np.sum(vector1.multiply(row))) / (np.sqrt(vector1a.sum()) * np.sqrt(rowa.sum())))

            return pd.Series(sims, idxs)

    def get_k_similar(self, data, vector):
        """Returns two values - the indices of the top k similar items to the
        vector from the dataset, and a Series representing their similarity
        values to the vector. We find the top k items from the data which
        are highly similar to the vector.

        Arguments:
            data {DataFrame} -- dataset
            vector {Series} -- vector
        Returns:
            Index -- indices of the top k similar items to the vector
            Series -- computed similarity of the top k similar items to the
            vector
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Normalize parameters data and vector
        # HINT: Use the normalize_data() function that we have defined in this
        # class
        normData = self.normalize_data(data, self.get_row_mean(data))
        normVector = self.normalize_data(vector, self.get_row_mean(vector))

        # TODO: Get the cosine similarity between the normalized data and
        # vector
        # HINT: Use the get_cosine_similarity() function that we have defined
        # in this class
        sim = self.get_cosine_similarity(normData, normVector)

        # TODO: Get the INDICES of the top k most similar items based on
        # the cosine similarity values
        # HINT: Use pandas.Series.nlargest() function.
        largest = sim.nlargest(self.k)

        # TODO: Return 2 values. See function comment
        return [[largest[largest == largest.iloc[0]].index[0], largest[largest == largest.iloc[1]].index[0]], largest]

    def get_rating(self, data, index, column):
        """Returns the extrapolated rating for the item in row index from the
        user in column column based on similar items.

        The algorithm for this function is as follows:
        1. Get k similar items.
        2. Compute for the rating using the similarity values and the raw
        ratings for the k similar items.

        Arguments:
            data {DataFrame} -- dataset
            index {int} -- row of the item
            column {int} -- column of the user
        Returns:
            np.float64 -- extrapolated rating based on similar ratings
        """

        # TODO: Complete this function.

        before_df = data.iloc[:index, :]
        after_df = data.iloc[index + 1:, :]
        new_data = pd.concat([before_df, after_df])
        vector = data.iloc[index, :]

        # TODO: Get top k items that are similar to the parameter vector
        # HINT: Use the get_k_similar() function that we have defined in this
        # class
        top = self.get_k_similar(new_data, vector)

        # TODO: Compute for the rating using the similarity values and the raw
        # ratings for the k similar items.

        info1 = top[0][0]
        info1 = [np.float(s) for s in info1.split() if s.isdigit()][0]
        info2 = top[0][1]
        info2 = [np.float(s) for s in info2.split() if s.isdigit()][0]
        sim1 = top[1].iloc[0]
        sim2 = top[1].iloc[1]

        rating = ((info1 * sim1) + (info2 * sim2)) / (sim1 + sim2)

        return rating
