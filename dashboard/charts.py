import plotly.graph_objects as go


class CandlestickChart:

    @staticmethod
    def build(df, symbol):

        fig = go.Figure()

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=df["datetime"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name=symbol,
                increasing_line_color="#00C853",
                decreasing_line_color="#FF1744",
            )
        )

        # EMA 20
        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["EMA_20"],
                mode="lines",
                name="EMA 20",
                line=dict(width=1.5)
            )
        )

        # EMA 50
        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["EMA_50"],
                mode="lines",
                name="EMA 50",
                line=dict(width=1.5)
            )
        )

        # EMA 200
        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["EMA_200"],
                mode="lines",
                name="EMA 200",
                line=dict(width=2)
            )
        )

        fig.update_layout(
            title=f"{symbol} Price Chart",
            template="plotly_dark",
            height=700,
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
            legend=dict(
                orientation="h",
                y=1.02,
                x=0
            ),
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10,
            ),
        )

        return fig