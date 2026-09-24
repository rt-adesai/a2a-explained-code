import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.helpers import new_task_from_user_message, new_text_message
from a2a.types import Part, TaskState
from a2a.utils.errors import (
    InternalError,
    InvalidParamsError,
    UnsupportedOperationError,
)

from app.agent import CurrencyAgent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CurrencyAgentExecutor(AgentExecutor):
    """Currency Conversion AgentExecutor Example."""

    def __init__(self):
        self.agent = CurrencyAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        error = self._validate_request(context)
        if error:
            raise InvalidParamsError()

        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task_from_user_message(context.message)  # type: ignore
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        try:
            async for item in self.agent.stream(query, task.context_id):
                is_task_complete = item['is_task_complete']
                require_user_input = item['require_user_input']

                if not is_task_complete and not require_user_input:
                    await updater.update_status(
                        TaskState.TASK_STATE_WORKING,
                        new_text_message(
                            item['content'],
                            context_id=task.context_id,
                            task_id=task.id,
                        ),
                    )
                elif require_user_input:
                    await updater.update_status(
                        TaskState.TASK_STATE_INPUT_REQUIRED,
                        new_text_message(
                            item['content'],
                            context_id=task.context_id,
                            task_id=task.id,
                        ),
                    )
                    break
                else:
                    await updater.add_artifact(
                        [Part(text=item['content'])],
                        name='conversion_result',
                    )
                    await updater.complete()
                    break

        except Exception as e:
            logger.error(f'An error occurred while streaming the response: {e}')
            raise InternalError() from e

    def _validate_request(self, context: RequestContext) -> bool:
        return False

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise UnsupportedOperationError()
