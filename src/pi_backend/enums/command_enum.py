from enum	import Enum


class CommandEnum(Enum):
	
	"""RPC 指令名枚举 (与 server 返回的 command 字段值一致)"""
	
	# Prompting
	PROMPT				= "prompt"
	STEER				= "steer"
	FOLLOW_UP			= "follow_up"
	ABORT				= "abort"
	CLEAR_QUEUE			= "clear_queue"
	NEW_SESSION			= "new_session"
	
	# State
	GET_STATE			= "get_state"
	GET_MESSAGES		= "get_messages"
	
	# Model
	SET_MODEL			= "set_model"
	CYCLE_MODEL			= "cycle_model"
	GET_AVAILABLE_MODELS	= "get_available_models"
	
	# Thinking
	SET_THINKING_LEVEL			= "set_thinking_level"
	CYCLE_THINKING_LEVEL		= "cycle_thinking_level"
	GET_AVAILABLE_THINKING_LEVELS	= "get_available_thinking_levels"
	
	# Queue Modes
	SET_STEERING_MODE	= "set_steering_mode"
	SET_FOLLOW_UP_MODE	= "set_follow_up_mode"
	
	# Compaction
	COMPACT				= "compact"
	SET_AUTO_COMPACTION	= "set_auto_compaction"
	
	# Retry
	SET_AUTO_RETRY		= "set_auto_retry"
	ABORT_RETRY			= "abort_retry"
	
	# Bash
	BASH				= "bash"
	ABORT_BASH			= "abort_bash"
	
	# Session
	GET_SESSION_STATS		= "get_session_stats"
	EXPORT_HTML				= "export_html"
	SWITCH_SESSION			= "switch_session"
	FORK					= "fork"
	CLONE					= "clone"
	GET_FORK_MESSAGES		= "get_fork_messages"
	GET_ENTRIES				= "get_entries"
	GET_TREE				= "get_tree"
	GET_LAST_ASSISTANT_TEXT	= "get_last_assistant_text"
	SET_SESSION_NAME		= "set_session_name"
	
	# Commands
	GET_COMMANDS		= "get_commands"