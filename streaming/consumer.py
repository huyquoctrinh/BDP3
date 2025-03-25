from kafka import KafkaConsumer
import json
# from db_handler import AtlasClient
import sys
import dotenv
import logging
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from json import loads
from time import time
import multiprocessing
# from data_model.review_model import CoreDMS, BaseCoreDMS, process_stream_data
# from data_model.tenant_model import TenantModel
# from data_model.log_model import LogModel

logging.basicConfig(
    filename = "./logs/data_updater.log",
    filemode = 'a',
    level = logging.INFO,
)

logger = logging.getLogger('data_updater')
dotenv.load_dotenv()

class DataUpdater:
    def __init__(self, 
        topic,
        kafka_broker = 'kafka:29092', 
    ):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_broker,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: loads(m.decode('utf-8'))
        )
        self.topic = topic

    
    def consume(self):
        # try:
            times = []
            obj_size = []
            for message in self.consumer:
                metadata_dict = message.value
                start = time()
                logger.info(f"Inserted metadata for {metadata_dict}")
            

if __name__ == "__main__":
    logger.info('Data updater started')
    data_updater = DataUpdater(topic='test')
    num_processes = 4

    for _ in range(num_processes):
        process = multiprocessing.Process(target=data_updater.consume)
        process.start()
        data_updater.consume()