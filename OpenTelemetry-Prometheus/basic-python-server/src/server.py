from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from prometheus_client import start_http_server
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


app = Flask(__name__)

_INF = float("inf")

"""
step 1. setup the prometheus client for opentelemetry we have to open a seperate 
demaon thread to run the WSGI server for metric export

Warning : if using prometheus_client also with the opentelemetry then save metric will be expose twise 
for default prometheus client metrics from both the ports
"""

start_http_server(port=6000, addr="0.0.0.0")

"""
step 2. define a resource
"""
resource = Resource(attributes={SERVICE_NAME: "flask-service"})

# Initialize PrometheusMetricReader which pulls metrics from the SDK
# on-demand to respond to scrape requests
prefix = "adl_monitor"
reader = PrometheusMetricReader(prefix=prefix)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

# create a meter for global meter provider
meter = metrics.get_meter_provider().get_meter(
    "myapp",
    "0.1.2",
)


work_counter = meter.create_counter(
    "api_requests",
    "requests",
    "number of api requests",
)

## metrics push using prometheus client
graphs = {}
graphs["c"] = Counter(
    "python_request_operations_total", "The total number of processed requests"
)
graphs["h"] = Histogram(
    "python_request_duration_seconds",
    "Histogram for the duration in seconds.",
    buckets=(1, 2, 5, 6, 10, _INF),
)


@app.route("/")
def hello():
    start = time.time()
    # increment request count using prometheus client
    graphs["c"].inc()

    # add telementry info using opentelementry
    work_counter.add(1, {"work.type": "request-handling"})
    work_counter.add(1, {"model.type": "regression"})

    time.sleep(0.600)
    end = time.time()
    graphs["h"].observe(end - start)

    return "Hello World!"


@app.route("/metrics")
def requests_count():
    res = []
    for k, v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")
