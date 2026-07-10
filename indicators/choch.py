class CHOCHIndicator:

    @staticmethod
    def calculate(df):

        df = df.copy()

        df["CHOCH"] = False
        df["CHOCH_DIRECTION"] = None

        last_bos = None

        for i in range(len(df)):

            bos = df.at[df.index[i], "BOS"]
            direction = df.at[df.index[i], "BOS_DIRECTION"]

            if not bos:
                continue

            if last_bos is None:
                last_bos = direction
                continue

            if direction != last_bos:

                df.at[df.index[i], "CHOCH"] = True
                df.at[df.index[i], "CHOCH_DIRECTION"] = direction

            last_bos = direction

        return df