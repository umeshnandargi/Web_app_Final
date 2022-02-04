from re import L
from flask import render_template, Flask, request, flash, Response
from math import sin, cos, tan, cosh, sinh, tanh, exp, pi
from camera import Video
import requests


def gen(camera):
    while True:
        data = camera.get_frame()
        frame = data[0]
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



app = Flask(__name__)
app.secret_key = "umeshnandargi"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nmo")
def nmo():
    return render_template("nmo.html")

@app.route("/gl2p", methods = ["POST", "GET"])
def gl2p():
    try:
        fun= request.form.get("function")
        ul = request.form.get("upper_limit")
        ll = request.form.get("lower_limit")
        function = lambda x: eval(fun)
        a, b = (float(eval(ul)) - float(eval(ll))) / 2, (float(eval(ul))+ float(eval(ll))) / 2
        u1, u2 = -a / (3 ** 0.5) + b, a / (3 ** 0.5) + b
        I = a * (function(u1) + function(u2))
        flash(f'Integration of {fun} from {ll} to {ul} using GL2P method is {I}')
        return render_template("gl2p.html", fun = fun)
    except:
        fun = False
        return render_template("gl2p.html", fun = fun)


@app.route("/gl3p", methods = ["POST", "GET"])
def gl3p():
    try:
        fun= request.form.get("function")
        ul = request.form.get("upper_limit")
        ll = request.form.get("lower_limit")
        function = lambda x: eval(fun)
        a, b = (float(eval(ul)) - float(eval(ll))) / 2, (float(eval(ul))+ float(eval(ll))) / 2
        u1, u2, u3 = a * (3 / 5) ** 0.5 + b, b, -a * (3 / 5) ** 0.5 + b
        I = ((5 / 9) * (function(u1)) + (8 / 9) * (function(u2)) + (5 / 9) * (function(u3))) * a
        flash(f'Integration of {fun} from {ll} to {ul} using GL3P method is {I}')
        return render_template("gl3p.html", fun = fun)
    except:
        fun = False
        return render_template("gl3p.html", fun = fun)


@app.route("/sim13", methods = ["POST", "GET"])
def sim13():
    try:
        fun= request.form.get("function")
        ul = request.form.get("upper_limit")
        ll = request.form.get("lower_limit")
        strips= request.form.get("n")
        function = lambda x: eval(fun)
        sum = 0
        x1 = float(eval(ll))
        xn = float(eval(ul))
        n = int(strips)
        h = (xn - x1) / n
        for i in range(1, n + 1, 2):
            sum = sum + function(x1) + 4 * function(x1 + h) + function(x1 + 2 * h)
            x1 += 2 * h
        I = sum * h / 3
        flash(f"Integration of {fun} within limits {ll} to {ul} with {n} no. of strips using Simpson's 1/3rd Rule is {I}")
        return render_template("sim13.html", fun = fun)
    except:
        fun = False
        return render_template("sim13.html", fun = fun)

@app.route("/sim38", methods = ["POST", "GET"])
def sim38():
    try:
        fun= request.form.get("function")
        ul = request.form.get("upper_limit")
        ll = request.form.get("lower_limit")
        strips= request.form.get("n")
        function = lambda x: eval(fun)
        sum = 0
        x1 = float(eval(ll))
        xn = float(eval(ul))
        n = int(strips)
        h = (xn - x1) / n
        for i in range(1, n + 1, 3):
            sum = sum + function(x1) + 3 * function(x1 + h) + 3 * function(x1 + 2 * h) + function(x1 + 3 * h)
            x1 += 3 * h
        I = sum * h * 3 / 8
        flash(f"Integration of {fun} within limits {ll} to {ul} with {n} no. of strips using Simpson's 3/8 Rule is {I}")
        return render_template("sim38.html", fun = fun)
    except:
        fun = False
        return render_template("sim38.html", fun = fun)


@app.route("/trap", methods = ["POST", "GET"])
def trap():
    try:
        fun= request.form.get("function")
        ul = request.form.get("upper_limit")
        ll = request.form.get("lower_limit")
        strips= request.form.get("n")
        function = lambda x: eval(fun)
        sum = 0
        x1 = float(eval(ll))
        xn = float(eval(ul))
        n = int(strips)
        h = (xn - x1) / n
        for i in range(1, n + 1):
            sum = sum + (h / 2) * (function(x1) + function(x1 + h))
            x1 += h
        I = sum
        flash(f"Integration of {fun} within limits {ll} to {ul} with {n} no. of strips using Trapezoidal Rule is {I}")
        return render_template("trap.html", fun = fun)
    except:
        fun = False
        return render_template("trap.html", fun = fun)

@app.route('/res',methods = ['POST','GET'])
def res():
    return render_template("video.html")


@app.route('/video')
def video():
    return Response(gen(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/weather', methods = ["POST", "GET"])
def weather():
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        API_key = '7eb1f8c7bda4c85046993ddbc3a32f9b'

        city = request.form.get("city_nm")

        request_url = f"{base_url}?appid={API_key}&q={city}"
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            # print(data)
            weather_data = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            t, t_fl, t_min, t_max = round(data["main"]['temp']-273.15, 2), round(data["main"]['feels_like'] -273.15, 2),\
                round(data["main"]['temp_min'] - 273.15, 2) , \
                round(data["main"]['temp_max']-273.15, 2)
        
        # date = "Friday, 04 February 2022"
        
        if t>30:
            filename = 'Hot.jpg'
        elif 10<t<35:
            filename = 'Medium.jpg'
        else:
            filename = 'Cold.jpg'

        current_temp = t
        current_weather = weather_data
        hi_low = f'{t_max} °C / {t_min} °C'
        return render_template("weather.html", filename = filename, city=city, current_temp= current_temp,
        current_weather= current_weather,hi_low= hi_low, icon =icon )
    except:
        return "<h1><center> Please enter valid city name </h1>"

if __name__=="__main__":
    app.run(debug=True)