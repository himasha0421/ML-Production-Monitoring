## up and run jaeger using docker

```
docker run --rm --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.50
```

open telemetry auto instrumentation library only  capture the
boundries of the network requests. Incoming and Outgoing request calls.

## command to start the application 
```
opentelemetry-instrument --service fast.api uvicorn app:app
```


## add sperate trace span to special fucntions to track the runtime and debug
