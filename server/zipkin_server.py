from flask import Flask, request
from flask.logging import default_handler
from py_zipkin.zipkin import zipkin_span,ZipkinAttrs
from transport import default_handler
from crawl_tiki import get_comment
from model import ClassifierModel

PORT = 1010

app = Flask(__name__)


@zipkin_span(service_name="get_comment", span_name= "get_comment")
def get_comment_from_url(url):
    return get_comment(url)

@zipkin_span(service_name="predict", span_name= "predict")
def predict(total_comment: list):
    model = ClassifierModel(path_model="aftifact/LR_Model.pkl", path_tokenzier="aftifact/tfidf.pkl", total_comment= total_comment)
    model.load_model()
    return model.counting_sentiment()

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/predict')
def index():
    with zipkin_span(
            service_name='latency_monitor',
            zipkin_attrs=ZipkinAttrs(
                trace_id=request.headers['X-B3-TraceID'],
                span_id=request.headers['X-B3-SpanID'],
                parent_span_id=request.headers['X-B3-ParentSpanID'],
                flags=request.headers['X-B3-Flags'],
                is_sampled=request.headers['X-B3-Sampled'],
            ),
            span_name='fetch_api',
            transport_handler=default_handler,
            port=PORT,
            sample_rate=100,  # 0.05, # Value between 0.0 and 100.0
    ):
        data = request.json
        comment = get_comment_from_url(data['url'])
        count_sentiment = predict(comment)
    return count_sentiment


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
