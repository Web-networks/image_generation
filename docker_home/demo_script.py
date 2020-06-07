import arrow
from bokeh.plotting import figure, output_file, show
import flask

def flask_example():
    app = flask.Flask("test")
    print("flask app created")


def arrow_example():
    dt = arrow.utcnow
    dt = dt().shift(hours=3)
    print(dt.format(), "is", dt.humanize())


def bokeh_example():
    factors = ["a", "b", "c", "d", "e", "f", "g", "h"]
    x =  [50, 40, 65, 10, 25, 37, 80, 60]

    dot = figure(title="Categorical Dot Plot", tools="", toolbar_location=None,
                y_range=factors, x_range=[0,100])

    dot.segment(0, factors, x, factors, line_width=2, line_color="green", )
    dot.circle(x, factors, size=15, fill_color="orange", line_color="green", line_width=3, )

    factors = ["foo 123", "bar:0.2", "baz-10"]
    x = ["foo 123", "foo 123", "foo 123", "bar:0.2", "bar:0.2", "bar:0.2", "baz-10",  "baz-10",  "baz-10"]
    y = ["foo 123", "bar:0.2", "baz-10",  "foo 123", "bar:0.2", "baz-10",  "foo 123", "bar:0.2", "baz-10"]
    colors = [
        "#0B486B", "#79BD9A", "#CFF09E",
        "#79BD9A", "#0B486B", "#79BD9A",
        "#CFF09E", "#79BD9A", "#0B486B"
    ]

    hm = figure(title="Categorical Heatmap", tools="hover", toolbar_location=None,
                x_range=factors, y_range=factors)

    hm.rect(x, y, color=colors, width=1, height=1)

    output_file("categorical.html", title="categorical.py example")
    print("wrote plot to categorical.html")

flask_example()
arrow_example()
bokeh_example()