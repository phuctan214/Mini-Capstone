import matplotlib.pyplot as plt
import requests
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span
import streamlit as st
from transport import default_handler
import ast

if __name__ == '__main__':
    with st.container():
        st.title("Mini Capstone TanNP3")
        st.subheader("User fill link refer to product which you want to buy, model will predict sentiment of total "
                     "comment")
        url = st.text_input('Please enter link')

        if st.button('Crawl Data'):
            with zipkin_span(
                    service_name='mini-capstone-tannp3',
                    span_name='zipkin-monitor',
                    transport_handler=default_handler,
                    sample_rate=100,  # 0.05, # Value between 0.0 and 100.0
            ):
                headers = {}
                headers.update(create_http_headers_for_new_span())
                response = requests.get('http://backend:1010/predict', headers=headers, json={"url": url})
                res = response.content.decode("utf-8")
                data = ast.literal_eval(res)
                sentiment = list(data.keys())
                count = list(data.values())

                fig = plt.figure(figsize=(10, 5))

                plt.barh(sentiment, count)
                plt.xlabel("Type Sentiment")
                plt.ylabel("Counting")
                plt.title("")

                st.pyplot(fig)
        else:
            st.write('Nothing to crawl')
