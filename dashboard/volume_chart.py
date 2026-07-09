import plotly.graph_objects as go


class VolumeChart:

    @staticmethod
    def build(df):

        colors = [
            "green" if c >= o else "red"
            for o, c in zip(df["open"], df["close"])
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=df["datetime"],
                y=df["volume"],
                marker_color=colors,
                name="Volume",
            )
        )

        fig.update_layout(
            title="Volume",
            template="plotly_dark",
            height=180,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10,
            ),
            showlegend=False,
        )

        return fig