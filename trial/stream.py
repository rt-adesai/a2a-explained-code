"""Send with the streaming call and print each event as it arrives (video 06, second half).

    python stream.py "How did Apple do over the last month?"
"""
import asyncio, sys
from a2a.client import create_client
from a2a.helpers import get_artifact_text, get_message_text, new_text_message
from a2a.types import Role, SendMessageRequest, TaskState

URL = "http://127.0.0.1:9999"


def name(state):
    return TaskState.Name(state).removeprefix("TASK_STATE_").lower()


async def main(text):
    client = await create_client(URL)
    request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER))
    async for event in client.send_message(request):
        if event.HasField("task"):
            print(f"task {event.task.id}: {name(event.task.status.state)}")
        elif event.HasField("status_update"):
            status = event.status_update.status
            note = get_message_text(status.message) if status.HasField("message") else ""
            print(f"status: {name(status.state)}  {note}")
        elif event.HasField("artifact_update"):
            artifact = event.artifact_update.artifact
            print(f"artifact {artifact.name}:\n{get_artifact_text(artifact)}")


asyncio.run(main(sys.argv[1]))
