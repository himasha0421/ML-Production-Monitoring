from fastapi import FastAPI
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# app manual opentelemetry traces
provider = TracerProvider()
# sets the global default tracer provider
trace.set_tracer_provider(provider)
# create a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)
# Done initialization OTEL


app = FastAPI()


@app.get("/")
def get_homepage():
    count = 1
    while count <= 3:
        # to trace a sub action we have to use opentelemetry trace span
        with tracer.start_as_current_span(f"loop-count-{count}") as span:
            print("Loop count : ", count)
            count += 1
            time.sleep(1)

    return {"status": 200, "target": "task completed."}
