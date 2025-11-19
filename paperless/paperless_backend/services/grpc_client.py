import logging

logger = logging.getLogger(__name__)


def generate_pdf_via_grpc(template_id, data, orientation="portrait"):
    import grpc
    from ..proto import pdf_generator_pb2, pdf_generator_pb2_grpc

    logger.info("Connecting to gRPC server at localhost:50051")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pdf_generator_pb2_grpc.PDFGeneratorStub(channel)
        logger.info("Stub created, sending request...")

        request = pdf_generator_pb2.PDFRequest(
            html_content=data, file_name=f"{template_id}.pdf", orientation=orientation
        )
        response = stub.GeneratePDF(request)
        logger.info("Received response from gRPC server")

        return response.pdf_data
