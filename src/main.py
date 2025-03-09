# from fastapi import FastAPI
# from src.routes import router
# import uvicorn
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
#
# # Set up TracerProvider
# trace_provider = TracerProvider()
# trace.set_tracer_provider(trace_provider)
#
# # Set up Console Exporter
# span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# trace_provider.add_span_processor(span_processor)
#
# # Initialize FastAPI app
# app = FastAPI()
#
# # Instrument FastAPI (Automatically traces all routes)
# FastAPIInstrumentor.instrument_app(app)
#
# # Include all routers
# app.include_router(router)
#
# @app.get("/")
# def read_root():
#     return {"message": "Hello, OpenTelemetry!"}
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)

from fastapi import FastAPI
from src.routes import router
import uvicorn
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Define Service Name
SERVICE_NAME = "my-fastapi-service"

# Set up TracerProvider with service name
trace_provider = TracerProvider()
trace.set_tracer_provider(trace_provider)

# Set up OTLP Exporter for Grafana Tempo
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4318/v1/traces")
span_processor = SimpleSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)

# Console Exporter for debugging
console_exporter = ConsoleSpanExporter()
trace_provider.add_span_processor(SimpleSpanProcessor(console_exporter))

# Initialize FastAPI app
app = FastAPI()

# Instrument FastAPI (Automatically traces all routes)
FastAPIInstrumentor.instrument_app(app)

# Include all routers
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello, OpenTelemetry with Grafana!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

