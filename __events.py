import asyncio
from nats.aio.client import Client as NATS

async def run(loop):
    nc = NATS()

    await nc.connect("127.0.0.1", loop=loop)

    async def help_request(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        

    # Use queue named 'workers' for distributing requests
    # among subscribers.
    await nc.subscribe("s3_file_update", "workers", help_request)

    print("Listening for requests on 's3_file_update' subject...")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()
    loop.close()