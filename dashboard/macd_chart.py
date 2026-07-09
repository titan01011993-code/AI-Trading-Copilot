import plotly.graph_objects as go


class MACDChart:

    @staticmethod
    def build(df):

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=df["datetime"],
                y=df["MACD_HIST"],
                name="Histogram",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["MACD"],
                name="MACD",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["MACD_SIGNAL"],
                name="Signal",
            )
        )

        fig.update_layout(
            title="MACD",
            template="plotly_dark",
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10,
            ),
            showlegend=True,
        )

        return fig