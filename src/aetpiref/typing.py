import sys
from datetime import datetime
from typing import Callable, Literal, Awaitable, Union, Any

if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class AETPIVersions(TypedDict):
    spec_version: str
    version: Literal["1.0"]


class TaskScope(TypedDict, total=False):
    id: str | None

    activity_id: str | None
    activity_instance_id: str | None

    execution_id: str | None
    error_message: str | None

    business_key: str | None
    topic_name: str | None

    process_definition_id: str | None
    process_definition_key: str | None
    process_definition_version_tag: str | None
    process_instance_id: str | None

    tenant_id: str | None

    retries: int | None
    suspended: bool | None

    priority: int | None

    worker_id: str | None

    lock_expiration_time: datetime | None

    # task properties related
    retry_timeout: int | None
    lock_duration: int | None
    title: str | None
    description: str | None


class ExternalTaskScope(TypedDict, total=False):
    type: Literal["externaltask"]
    protocol: Literal["camunda7", "camunda8"]
    aetpi: AETPIVersions
    task: TaskScope


class Capability(TypedDict):
    """
    A capability handled by the application
    """

    topic_name: (
        str | None
    )  # camunda defines this as nullable, but it is required in yio
    process_definition_key: str | None


class CapabilitiesScope(TypedDict, total=True):
    """
    Scope that is issued when handling application capabilities
    """

    type: Literal["capabilities"]
    aetpi: AETPIVersions
    state: dict[str, Any]


# Phases of an external task
# 1) Request: -> Lock or not
# 2) Execute: -> Fetch vars
class CapabilitiesRequestEvent(TypedDict):
    """
    Event that is issued to query for application capabilities
    (external task topics capable to handle)
    """

    type: Literal["capabilities.request"]


class CapabilitiesResponseEvent(TypedDict):
    """
    Event that is issued to announce application capabilities
    (external task topics capable to handle)
    """

    type: Literal["capabilities.response"]
    capabilities: list[Capability]


class ExternalTaskStartEvent(TypedDict):
    """
    Event that is issued to the application to indicate beginning
    of an external task processing.
    usually immediately followed by a lock request
    """

    type: Literal["externaltask.start"]


class ExternalTaskEndEvent(TypedDict):
    """
    Event that is issued to the application to indicate the end
    of an external task processing.
    The application should release any resources associated with the task
    no further events will be sent for this task, and the application might
    get an abortion if it does not respond to this event by stopping.
    """

    type: Literal["externaltask.end"]


class ExternalTaskLockRequestEvent(TypedDict):
    """
    Event that is issued to the application to check if the task
    should be locked (and therefore executed)
    """

    type: Literal["externaltask.lock.request"]


class ExternalTaskLockAcceptEvent(TypedDict):
    """
    Event that is received if the application accepts the task
    for lock
    """

    type: Literal["externaltask.lock.accept"]
    lock_duration: int  # the lock duration in milliseconds


class ExternalTaskLockRejectEvent(TypedDict):
    """
    Event that is received if the application rejects the task
    for lock

    """

    type: Literal["externaltask.lock.reject"]
    reason_code: Literal["NOT_IMPLEMENTED", "RESOURCE_UNAVAILABLE", "CUSTOM"]
    reason_message: str


class ExternalTaskExecuteRequestEvent(TypedDict):
    """
    Event that is issued to the application to execute the task
    """

    type: Literal["externaltask.execute.request"]


class ExternalTaskExecuteRejectEvent(TypedDict):
    """
    Event that is received if the application rejects the task
    for execution
    """

    type: Literal["externaltask.execute.reject"]
    reason_code: Literal["NOT_IMPLEMENTED", "RESOURCE_UNAVAILABLE", "CUSTOM"]
    reason_message: str


class ExternalTaskExecuteAcceptEvent(TypedDict):
    """
    Event that is received if the application accepts the task
    for execution
    """

    type: Literal["externaltask.execute.accept"]
    # required_variables:
    #   None: all variables are required
    #   empty set: no variables are required
    #   set: only the variables in the set are required
    required_variables: set[str] | None


class ExternalTaskExecuteStartEvent(TypedDict):
    """
    Event that is issued to the application to start the execution
    """

    type: Literal["externaltask.execute.start"]
    variables: dict[str, Any]


class ExternalTaskExecuteCompleteEvent(TypedDict):
    """
    Event that is sent to the server to indicate that the task has been completed
    """

    type: Literal["externaltask.execute.complete"]
    variables: dict[str, Any] | None


class ExternalTaskExecuteAbortEvent(TypedDict):
    """
    Event that is sent to the server to indicate that the task has been aborted
    """

    type: Literal["externaltask.execute.abort"]


class ExternalTaskExecuteFailureEvent(TypedDict):
    """
    Event that is received if the application rejects the task
    for execution
    """

    type: Literal["externaltask.execute.failure"]
    error_message: str | None
    error_details: str | None
    retries: int | None
    retry_timeout: int | None  # timeout in milliseconds
    variables: dict[str, Any] | None
    local_variables: dict[str, Any] | None


class ExternalTaskExecuteBusinessErrorEvent(TypedDict):
    """
    Event that is received if the application rejects the task
    for execution
    """

    type: Literal["externaltask.execute.error"]
    error_code: str | None
    error_message: str | None
    variables: dict[str, Any] | None


class ExternalTaskExtendLockEvent(TypedDict):
    """
    Event triggered by an aetpi application if the lock of an external task
    should be extended (e.g. because the job takes more time then expected)
    """

    type: Literal["externaltask.execute.extendlock"]
    lock_duration: int


class LifespanScope(TypedDict, total=True):
    type: Literal["lifespan"]
    aetpi: AETPIVersions
    state: dict[str, Any]


class LifespanStartupEvent(TypedDict):
    type: Literal["lifespan.startup"]
    state: dict[str, Any]


class LifespanStartupCompleteEvent(TypedDict):
    type: Literal["lifespan.startup.complete"]


class LifespanStartupFailedEvent(TypedDict):
    type: Literal["lifespan.startup.failed"]
    message: str


class LifespanShutdownEvent(TypedDict, total=True):
    type: Literal["lifespan.startup"]
    state: dict[str, Any]


class LifespanShutdownCompleteEvent(TypedDict, total=True):
    type: Literal["lifespan.startup.complete"]


class LifespanShutdownFailedEvent(TypedDict, total=True):
    type: Literal["lifespan.startup.failed"]
    message: str


AETPIReceiveEvent = Union[
    ExternalTaskStartEvent,
    ExternalTaskEndEvent,
    ExternalTaskLockRequestEvent,
    ExternalTaskExecuteRequestEvent,
    ExternalTaskExecuteStartEvent,
    # Request for startup
    LifespanStartupEvent,
    LifespanShutdownEvent,
    # Request for capabilities
    CapabilitiesRequestEvent,
]
AETPISendEvent = Union[
    # Answer to LockRequest
    ExternalTaskLockAcceptEvent,
    ExternalTaskLockRejectEvent,
    # Answer to ExecuteRequest
    ExternalTaskExecuteAcceptEvent,
    ExternalTaskExecuteRejectEvent,
    # Answer to ExecuteStart
    ExternalTaskExecuteCompleteEvent,
    ExternalTaskExecuteFailureEvent,
    ExternalTaskExecuteBusinessErrorEvent,
    ExternalTaskExecuteAbortEvent,
    # Others
    ExternalTaskExtendLockEvent,
    # Answer to lifespan events
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
    # Answer to capabilities
    CapabilitiesResponseEvent,
]

AETPIScope = ExternalTaskScope | LifespanScope | CapabilitiesScope
AETPIReceiveCallable = Callable[[], Awaitable[AETPIReceiveEvent]]
AETPISendCallable = Callable[[AETPISendEvent], Awaitable[None]]

# Asynchronous External Task Processor Interface
AETPIApplication = Callable[
    [AETPIScope, AETPIReceiveCallable, AETPISendCallable], Awaitable[None]
]
