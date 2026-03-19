import logging
import sys

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter


def setup_logger(service_name: str) -> logging.Logger:

    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0"
    })

    provider = LoggerProvider(resource=resource)

    provider.add_log_record_processor(
        BatchLogRecordProcessor(
            OTLPLogExporter(endpoint="http://localhost:4320/v1/logs") 
        )
    )

    otel_handler = LoggingHandler(
        level=logging.NOTSET,
        logger_provider=provider
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s  [%(levelname)-8s]  %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
    )

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(otel_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger