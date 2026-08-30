from easy_factory	import BaseModelFactory

from ..models	import (
	# Agent
	AgentStartEvent,
	AgentEndEvent,
	AgentSettledEvent,
	# Turn
	TurnStartEvent,
	TurnEndEvent,
	# Message
	MessageStartEvent,
	MessageUpdateEvent,
	MessageEndEvent,
	# Bash
	BashExecutionUpdateEvent,
	# Tool
	ToolExecutionStartEvent,
	ToolExecutionUpdateEvent,
	ToolExecutionEndEvent,
	# Queue
	QueueUpdateEvent,
	# Compaction
	CompactionStartEvent,
	CompactionEndEvent,
	# Auto Retry
	AutoRetryStartEvent,
	AutoRetryEndEvent,
	# Summarization Retry
	SummarizationRetryScheduledEvent,
	SummarizationRetryAttemptStartEvent,
	SummarizationRetryFinishedEvent,
	# Extension
	ExtensionErrorEvent,
	ExtensionUIRequestEvent,
)


events_factory = BaseModelFactory()

# 事件模型注册顺序仅影响同名匹配时的优先级。
# 每个事件 type 为唯一 Literal, 正常分发下顺序无关; 若未来出现字段重叠的模型,
# 需将更具体的模型优先注册 (priority=0 或先注册)。

# Agent
events_factory.register(AgentStartEvent)
events_factory.register(AgentEndEvent)
events_factory.register(AgentSettledEvent)

# Turn
events_factory.register(TurnStartEvent)
events_factory.register(TurnEndEvent)

# Message
events_factory.register(MessageStartEvent)
events_factory.register(MessageUpdateEvent)
events_factory.register(MessageEndEvent)

# Bash
events_factory.register(BashExecutionUpdateEvent)

# Tool
events_factory.register(ToolExecutionStartEvent)
events_factory.register(ToolExecutionUpdateEvent)
events_factory.register(ToolExecutionEndEvent)

# Queue
events_factory.register(QueueUpdateEvent)

# Compaction
events_factory.register(CompactionStartEvent)
events_factory.register(CompactionEndEvent)

# Auto Retry
events_factory.register(AutoRetryStartEvent)
events_factory.register(AutoRetryEndEvent)

# Summarization Retry
events_factory.register(SummarizationRetryScheduledEvent)
events_factory.register(SummarizationRetryAttemptStartEvent)
events_factory.register(SummarizationRetryFinishedEvent)

# Extension
events_factory.register(ExtensionErrorEvent)
events_factory.register(ExtensionUIRequestEvent)


__all__ = [
	
	"events_factory",
	
]