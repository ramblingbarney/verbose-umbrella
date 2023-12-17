from flask import Flask, render_template, request, Response

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from pytrends.request import TrendReq
import io

app = Flask(__name__)

pytrends = TrendReq(
    hl="en-US",
    tz=360,
    timeout=(10, 25),
    retries=2,
    backoff_factor=0.1,
    requests_args={"verify": False},
)


@app.route("/")
def index():
    term_str = request.args.get("terms", default="*", type=str)
    terms = term_str.split(",")
    pytrends.build_payload(terms, cat=0, timeframe="today 3-m", geo="ES")
    gtrend_result_over_time = pytrends.interest_over_time()

    image_1 = gtrend_result_over_time.plot(figsize=(12, 10), y=terms)
    fig_ot = image_1.get_figure()
    fig_ot.savefig("static/images/ot_plot.png")

    gtrend_result_interest_by_region = pytrends.interest_by_region(
        resolution="CITY", inc_low_vol=True, inc_geo_code=False
    )

    image_2 = gtrend_result_interest_by_region.plot(
        figsize=(12, 10), y=terms, kind="bar"
    )
    fig_2 = image_2.get_figure()
    fig_2.savefig("static/images/i_plot.png")

    return render_template(
        "index.html",
        url_ot="static/images/ot_plot.png",
        url_i="static/images/i_plot.png",
        terms=term_str,
    )
