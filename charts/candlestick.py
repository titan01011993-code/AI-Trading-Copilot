import plotly.graph_objects as go


class CandlestickChart:

    @staticmethod
    def build(df, symbol):

        fig = go.Figure()

        fig.add_trace(

            go.Candlestick(

                x=df["datetime"],

                open=df["open"],

                high=df["high"],

                low=df["low"],

                close=df["close"],

                name=symbol

            )

        )

        fig.update_layout(

            title=symbol,

            xaxis_rangeslider_visible=False,

            template="plotly_dark",

            height=650

        )

        return fig