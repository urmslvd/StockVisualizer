from flask import Flask, render_template, request

global code
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")
        

@app.route('/data/', methods = ['POST'])
def data():
    if request.method == 'POST':

        code = request.form["code_name"]

        from pandas_datareader import data
        import datetime
        from bokeh.plotting import figure, show, output_file
        from bokeh.embed import components
        from bokeh.resources import CDN

        start = datetime.datetime(2000, 11, 1)
        end = datetime.datetime(2025, 1, 1)

        #name = input("Code: ").upper()

        df = data.DataReader(name = code.upper(), data_source = "yahoo", start = start, end = end) 

        def inc_dec(c, o):
            if c > o:
                value = "Increase"
            elif c < o:
                value = "Decrease"
            else:
                value = "Equal"
            return value

        df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]

        df["Middle"] = (df.Open + df.Close)/2

        df["Height"] = abs(df.Close - df.Open)/2

        hours_12 = 12*60*60*1000

        p = figure(x_axis_type = 'datetime', width = 1000, height = 400, sizing_mode = "scale_width")
        p.title.text = "Stock Data, heuheu"
        p.grid.grid_line_alpha = 0.3

        p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"], 
            hours_12, df.Height[df.Status == "Increase"], fill_color = "#FCA1A1", 
            line_color = "#FCA1A1")

        p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], 
            hours_12, df.Height[df.Status == "Decrease"], fill_color = "#AD0D0D", 
            line_color = "#AD0D0D")

        p.segment(df.index, df.High, df.index, df.Low, color = "#A95151" )

        script1, div1 = components(p)
        cdn_js = CDN.js_files[0]


        
        return render_template("data.html", script1 = script1,
        div1 = div1,
        cdn_js = cdn_js)

if __name__ == "__main__":
    app.run()