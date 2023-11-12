import asyncio
from aiohttp import web
import socketio
import cv2
import base64

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Initialize video capture
# You may need to adjust the index based on your camera setup
cap = cv2.VideoCapture(0)
print(cap.isOpened())


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def video_feed(request):
    return web.Response(content_type='multipart/x-mixed-replace; boundary=frame')


async def consume_video(websocket):
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to base64
        _, buffer = cv2.imencode('.jpg', frame)
        data = base64.b64encode(buffer.tobytes()).decode('utf-8')

        # Send the frame to the client
        await sio.send(websocket, data, room='example-room')

        # Introduce some delay here if needed
        await asyncio.sleep(0.1)


async def produce_video():
    pass

if __name__ == '__main__':
    app.router.add_get('/', index)
    app.router.add_get('/video_feed', video_feed)
    app.router.add_get('/ws', consume_video)
    web.run_app(app)
