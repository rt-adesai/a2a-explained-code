"""Tap the wire: print every HTTP request the client sends and what comes back (video 08).

    python wire.py "How did Apple do over the last month?"
"""
import asyncio, json, sys
import httpx
from google.protobuf.json_format import MessageToJson
from a2a.client import ClientConfig, create_client
from a2a.helpers import new_text_message
from a2a.types import GetTaskRequest, Role, SendMessageRequest

URL = "http://127.0.0.1:9999"


async def log_request(request):
    print(f"\n>>> {request.method} {request.url}")
    for key in ("a2a-version", "content-type", "accept"):
        if key in request.headers:
            print(f"    {key}: {request.headers[key]}")
    if request.content:
        print(json.dumps(json.loads(request.content), indent=2))


async def log_response(response):
    print(f"<<< {response.status_code} {response.headers.get('content-type')}")
    if "text/event-stream" not in response.headers.get("content-type", ""):
        await response.aread()
        print(json.dumps(response.json(), indent=2))


async def main(text):
    http = httpx.AsyncClient(timeout=120, event_hooks={"request": [log_request],
                                                       "response": [log_response]})
    client = await create_client(URL, ClientConfig(httpx_client=http))
    request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER))
    async for event in client.send_message(request):
        print(f"<<< event: {MessageToJson(event, indent=2)}")
        task_id = (event.task.id if event.HasField("task") else
                   event.status_update.task_id if event.HasField("status_update") else
                   event.artifact_update.task_id)
    await client.get_task(GetTaskRequest(id=task_id))


asyncio.run(main(sys.argv[1]))
