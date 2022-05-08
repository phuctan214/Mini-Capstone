import requests

def default_handler(encoded_span):
    return requests.post(
        'http://zipkin:9411/api/v1/spans',
        data=encoded_span,
        headers={'Content-Type': 'application/x-thrift'},
    )