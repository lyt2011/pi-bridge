from easy_factory	import BaseModelFactory

from ..models	import (
	# Prompting
	PromptResponse,
	SteerResponse,
	FollowUpResponse,
	AbortResponse,
	ClearQueueResponse,
	NewSessionResponse,
	# State
	StateResponse,
	GetMessagesResponse,
	# Model
	SetModelResponse,
	CycleModelResponse,
	GetAvailableModelsResponse,
	# Thinking
	SetThinkingLevelResponse,
	CycleThinkingLevelResponse,
	GetAvailableThinkingLevelsResponse,
	# Queue Modes
	SetSteeringModeResponse,
	SetFollowUpModeResponse,
	# Compaction
	CompactResponse,
	SetAutoCompactionResponse,
	# Retry
	SetAutoRetryResponse,
	AbortRetryResponse,
	# Bash
	BashResponse,
	AbortBashResponse,
	# Session
	GetSessionStatsResponse,
	ExportHtmlResponse,
	SwitchSessionResponse,
	ForkResponse,
	CloneResponse,
	GetForkMessagesResponse,
	GetEntriesResponse,
	GetTreeResponse,
	GetLastAssistantTextResponse,
	SetSessionNameResponse,
	# Commands
	GetCommandsResponse,
)


responses_factory = BaseModelFactory()

# 注意注册顺序与优先级:
# 各响应模型的 command 均为唯一 Literal 判别字段, 分发时严格按值匹配,
# 因此顺序不影响匹配正确性; 此处按分组顺序注册, 便于阅读与维护。
# 若将来出现可同时匹配同一数据的模型, 先注册者优先(priority=0 最优先)。

responses_factory.register(PromptResponse)
responses_factory.register(SteerResponse)
responses_factory.register(FollowUpResponse)
responses_factory.register(AbortResponse)
responses_factory.register(ClearQueueResponse)
responses_factory.register(NewSessionResponse)

responses_factory.register(StateResponse)
responses_factory.register(GetMessagesResponse)

responses_factory.register(SetModelResponse)
responses_factory.register(CycleModelResponse)
responses_factory.register(GetAvailableModelsResponse)

responses_factory.register(SetThinkingLevelResponse)
responses_factory.register(CycleThinkingLevelResponse)
responses_factory.register(GetAvailableThinkingLevelsResponse)

responses_factory.register(SetSteeringModeResponse)
responses_factory.register(SetFollowUpModeResponse)

responses_factory.register(CompactResponse)
responses_factory.register(SetAutoCompactionResponse)

responses_factory.register(SetAutoRetryResponse)
responses_factory.register(AbortRetryResponse)

responses_factory.register(BashResponse)
responses_factory.register(AbortBashResponse)

responses_factory.register(GetSessionStatsResponse)
responses_factory.register(ExportHtmlResponse)
responses_factory.register(SwitchSessionResponse)
responses_factory.register(ForkResponse)
responses_factory.register(CloneResponse)
responses_factory.register(GetForkMessagesResponse)
responses_factory.register(GetEntriesResponse)
responses_factory.register(GetTreeResponse)
responses_factory.register(GetLastAssistantTextResponse)
responses_factory.register(SetSessionNameResponse)

responses_factory.register(GetCommandsResponse)


__all__ = [
	
	"responses_factory",
	
]