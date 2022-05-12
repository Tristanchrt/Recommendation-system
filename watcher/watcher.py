import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pika

class Watcher:
    DIRECTORY_TO_WATCH = "./images"

    def __init__(self):
        self.observer = Observer()
        
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):


    @staticmethod
    def on_any_event(event):  
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            if "/metadata" in event.src_path:
                channel.basic_publish(exchange='', routing_key='metadata_updated', body='')
            elif "/images/images" in event.src_path:
                channel.basic_publish(exchange='', routing_key='images_updated', body='')
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            if "/metadata" in event.src_path:
                channel.basic_publish(exchange='', routing_key='metadata_updated', body='')
            elif "/images/images" in event.src_path:
                channel.basic_publish(exchange='', routing_key='images_updated', body='')

            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)

def main():
    w = Watcher()
    w.run()

if __name__ == '__main__':

    HOSTNAME = '0.0.0.0'
    PORT = 5672
    
    connection_params = pika.ConnectionParameters(host=HOSTNAME, port=PORT, socket_timeout=5)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='metadata_updated')
    channel.queue_declare(queue='image_updated')

    
    main()

