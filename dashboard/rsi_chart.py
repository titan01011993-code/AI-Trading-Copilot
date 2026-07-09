import plotly.graph_objects as go


class RSIChart:

    @staticmethod
    def build(df):

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["RSI"],
                name="RSI",
                line=dict(color="orange", width=2),
            )
        )

        fig.add_hline(
            y=70,
            line_dash="dash",
            line_color="red",
        )

        fig.add_hline(
            y=30,
            line_dash="dash",
            line_color="green",
        )

        fig.update_layout(
            title="RSI (14)",
            template="plotly_dark",
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10,
            ),
            xaxis_rangeslider_visible=False,
            showlegend=False,
        )

        fig.update_yaxes(
            range=[0, 100],
            tickvals=[0, 30, 50, 70, 100]
        )

        return fig