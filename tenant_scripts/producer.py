import pandas as pd 
import json
import time
from kafka import KafkaProducer

class DataProducer:
    def __init__(self, 
        topic,
        kafka_broker = 'localhost:9092', 
    ):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def produce(self, data):
        # print(data)
        self.producer.send(self.topic, value=data)
        self.producer.flush()
        print(f"Produced data: {data}")
    
if __name__ == "__main__":
    data_producer = DataProducer(topic='test')
    df = pd.read_csv('/home/trnhquchuy/BDP3/dataset/test.tsv', sep="\t", on_bad_lines="skip")
    for i in range(10):
        data = df.iloc[i].to_dict()
        data['tenant_id'] = "9"
        data_producer.produce(data)
        # data_producer.produce({
        #     "tenant_id": "9",
        #     "review": 
        # })
        time.sleep(1)
