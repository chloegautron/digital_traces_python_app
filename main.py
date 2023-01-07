import logging
from flask import Flask
import requests
from pytrends.request import TrendReq
from datetime import datetime


pytrends = TrendReq(hl='en-US', tz=360)

app = Flask(__name__)

@app.route('/', methods=["GET"])

def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=G-L4MNLKXJDK"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-L4MNLKXJDK');
    </script>
    """
    return prefix_google + "Hello World"

@app.route('/logger', methods=['GET','POST'])

def printMsg():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return "Check your console"

@app.route('/cookie', methods=['GET', 'POST'])
def cookie():
    req=requests.get('https://www.google.com/')
    return req.cookies.get_dict()

@app.route('/cookie/analytics', methods=['GET', 'POST'])
def cookie_analytics():
    req=requests.get('https://analytics.google.com/analytics/web/?hl=fr#/p345017433/reports/reportinghub')
    return req.text

kw_list = ["Blockchain"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 90-d', geo='', gprop='')


@app.route('/trend', methods=["GET","POST"])
def googletrendchart():
    topic_1 = "Football"
    topic_2 = "Football américain"
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=[topic_1, topic_2], timeframe='today 90-d', geo='FR')
    df = pytrends.interest_over_time()
    
    data_topic_1 = df[topic_1].tolist()
    data_topic_2 = df[topic_2].tolist()
    data_date = df.index.values.tolist()
    
    timestamp_in_seconds=[element/1e9 for element in data_date]
    date= [datetime.fromtimestamp(element) for element in timestamp_in_seconds]
    days=[element.date() for element in date]
    months=[element.isoformat() for element in days]
    params = {
        "type": 'line',
        "data": {
            "labels": months,
            "datasets": [{
                "label": topic_1,
                "data": data_topic_1,
                "borderColor": '#3e95cd',
                "fill": 'false',
            },
            {
                "label": topic_2,
                "data": data_topic_2,
                "borderColor": '#ffce56',
                "fill": 'false',
            }
            ]
        },
        "options": {
            "title": {
                "text": 'Comparaison entre'# + str(topic_1) + " et " + str(topic_2)
            },
            "scales": {
                "yAxes": [{
                     "ticks": {
                        "beginAtZero": 'true'
                    }
                }]
            }
        }
    }
                                        
    prefix_chartjs = """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
         <canvas id="myChart" width="1200px" height="700px"></canvas>""" + f"""
        <script>
        var ctx = document.getElementById('myChart');
        var myChart = new Chart(ctx, {params});
        </script>
        """
  
    return prefix_chartjs


if __name__ == '__main__':
    app.run(debug=True)
