import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio
from nats.aio.client import Client as NATS

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
                nc.publish("metadata_updated", b"")
            elif "/images/images" in event.src_path:
                nc.publish("images_updated",b"")
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            if "/metadata" in event.src_path:
                nc.publish("metadata_updated", b"")
            elif "/images/images" in event.src_path:
                nc.publish("images_updated", b"")
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)

async def main(loop):
    
    await nc.connect("127.0.0.1", loop=loop)
    w = Watcher()
    w.run()

if __name__ == '__main__':
    nc = NATS()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()
    loop.close()



   