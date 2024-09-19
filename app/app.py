'import time
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
import httpx

# Настройка ресурса с указанием имени сервиса
resource = Resource.create({"service.name": "test"})

# Настройка TracerProvider с ресурсом
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Настройка OTLP экспортера
otlp_exporter = OTLPSpanExporter(endpoint="http://alloy:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Настройка HTTP клиента
HTTPXClientInstrumentor().instrument()

def do_work():
    with tracer.start_as_current_span("work-span"):
        print("Doing work...")
        time.sleep(1)

def main():
    while True:
        do_work()

if __name__ == "__main__":
    main()
