"""Drop the connection while the analyst works, then come back for the brief (video 12).

    python reconnect.py "How did Apple do over the last month?"
"""
import asyncio, sys
import httpx
from a2a.client import ClientConfig, create_client
from a2a.helpers import get_artifact_text, get_message_text, new_text_message
from a2a.types import GetTaskRequest, Role, SendMessageRequest, SubscribeToTaskRequest, TaskState

URL = "http://127.0.0.1:9999"


def name(state):
    return TaskState.Name(state).removeprefix("TASK_STATE_").lower()


def show(event):
    if event.HasField("task"):
        print(f"task {event.task.id}: {name(event.task.status.state)}")
    elif event.HasField("status_update"):
        status = event.status_update.status
        note = get_message_text(status.message) if status.HasField("message") else ""
        print(f"status: {name(status.state)}  {note}")
    elif event.HasField("artifact_update"):
        print(f"artifact {event.artifact_update.artifact.name}: arrived")


async def main(text):
    # First connection: send, watch until the analyst is working, then hang up.
    async with httpx.AsyncClient(timeout=120) as http:
        client = await create_client(URL, ClientConfig(httpx_client=http))
        request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER))
        async for event in client.send_message(request):
            show(event)
            if event.HasField("status_update") and event.status_update.status.HasField("message"):
                task_id = event.status_update.task_id
                break
    print("-- client disconnected; the server keeps working --")
    await asyncio.sleep(3)

    # Second connection: subscribe to the same task and catch up.
    client = await create_client(URL)
    print("-- client back; subscribing to the task --")
    async for event in client.subscribe(SubscribeToTaskRequest(id=task_id)):
        show(event)
    task = await client.get_task(GetTaskRequest(id=task_id))
    print(f"task {task.id}: {name(task.status.state)}")
    for artifact in task.artifacts:
        print(f"  artifact {artifact.name}:\n{get_artifact_text(artifact)}")


asyncio.run(main(sys.argv[1]))
