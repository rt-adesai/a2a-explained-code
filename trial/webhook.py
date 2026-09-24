"""Register a webhook, send, hang up; the brief is delivered to the webhook (video 12, alternative).

    python webhook.py "How did Apple do over the last month?"
"""
import asyncio, sys
import uvicorn
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from a2a.client import ClientConfig, create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest, TaskPushNotificationConfig, TaskState

URL = "http://127.0.0.1:9999"
HOOK = "http://127.0.0.1:9998/hook"
finished = asyncio.Event()


async def hook(request):
    event = await request.json()
    print(f"webhook got (token {request.headers.get('x-a2a-notification-token')}): "
          f"{list(event)[0]}")
    if "statusUpdate" in event:
        print(f"  state {event['statusUpdate']['status']['state']}")
    if "artifactUpdate" in event:
        artifact = event["artifactUpdate"]["artifact"]
        print(f"  artifact {artifact['name']}:\n{artifact['parts'][0]['text']}")
    if "task" in event and event["task"]["status"]["state"] == "TASK_STATE_COMPLETED":
        for artifact in event["task"].get("artifacts", []):
            print(f"  artifact {artifact['name']}:\n{artifact['parts'][0]['text']}")
    if event.get("statusUpdate", {}).get("status", {}).get("state") == "TASK_STATE_COMPLETED":
        finished.set()
    if event.get("task", {}).get("status", {}).get("state") == "TASK_STATE_COMPLETED":
        finished.set()
    return Response()


async def main(text):
    app = Starlette(routes=[Route("/hook", hook, methods=["POST"])])
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=9998, log_level="warning"))
    serving = asyncio.create_task(server.serve())

    config = ClientConfig(streaming=False, polling=True,
                          push_notification_config=TaskPushNotificationConfig(url=HOOK, token="s3cret"))
    client = await create_client(URL, config)
    request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER))
    async for response in client.send_message(request):
        task = response.task
    print(f"task {task.id}: {TaskState.Name(task.status.state)}")
    await client.close()
    print("-- client hung up; waiting at the webhook --")
    await finished.wait()
    server.should_exit = True
    await serving


asyncio.run(main(sys.argv[1]))
