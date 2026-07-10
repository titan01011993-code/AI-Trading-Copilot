class VolumeFeatures:

    @staticmethod
    def calculate(df):

        data = df.copy()

        data["AVG_VOLUME"] = (

            data["volume"]

            .rolling(20)

            .mean()

        )

        data["VOLUME_RATIO"] = (

            data["volume"]

            /

            data["AVG_VOLUME"]

        )

        data["HIGH_VOLUME"] = (

            data["VOLUME_RATIO"]

            >

            1.5

        ).astype(int)

        return data