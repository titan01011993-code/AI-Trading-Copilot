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

                increasing_line_color="#00C853",

                decreasing_line_color="#FF1744",

                name=symbol,

            )

        )

        fig.update_layout(

            title=f"{symbol} Price Chart",

            template="plotly_dark",

            height=650,

            xaxis_rangeslider_visible=False,

            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10,
            ),

        )

        return fig