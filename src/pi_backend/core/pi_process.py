from typing				import Optional, List, Self
from asyncio.subprocess	import Process

import asyncio
import shutil


# 默认的pi路径
DEFAULT_PI_PATH: Optional[str] = shutil.which("pi")


class PIProcess:

	"""
	封装一些process的基本操作
	"""
	
	def __init__(self, pi_process: Process) -> None:
		
		self._process = pi_process
	
	@classmethod
	async def build_process(
		cls, *,
		pi_path			: Optional[str]			= DEFAULT_PI_PATH,
		session			: Optional[str]			= None,
		session_dir		: Optional[str]			= None,
		tools			: Optional[List[str]]	= None,
		system_prompt	: Optional[str]			= None,
	) -> Self:
		
		"""
		通过函数传入的参数 (不能用*或**) 构建进程实例
		通过进程实例实例化 cls
		返回 cls 的实例
		"""
		
		if pi_path is None:
			raise ValueError("未找到 pi 可执行文件，请传入 pi_path 或检查 PATH")
		
		args: List[str] = [pi_path, "--mode", "rpc"]
		
		if session is not None:
			args += ["--session", session]
		
		if session_dir is not None:
			args += ["--session-dir", session_dir]
		
		if tools is not None:
			args += ["--tools", ",".join(tools)]
		
		if system_prompt is not None:
			args += ["--system-prompt", system_prompt]
		
		process = await asyncio.create_subprocess_exec(
			*args,
			stdin	= asyncio.subprocess.PIPE,
			stdout	= asyncio.subprocess.PIPE,
			stderr	= asyncio.subprocess.DEVNULL,
		)
		
		return cls(process)
	
	async def read_line(self) -> str:
		
		"""
		读取 self._process 的缓冲区
		并返回 str
		"""
		
		line = await self._process.stdout.readline()
		
		if isinstance(line, bytes):
			return line.decode("utf-8")
		
		return line
	
	async def write_line(self, *lines: str) -> None:
		
		"""
		写一行(或多行)jsonl
		自动补齐 \n
		"""
		
		for jsonl in lines:
			
			if not jsonl.endswith("\n"):
				jsonl += "\n"
			
			self._process.stdin.write(jsonl.encode("utf-8"))
			await self._process.stdin.drain()
	
	async def close_process(self) -> None:
	
		"""
		关闭 self._process
		释放进程与FD
		"""
		
		if self._process.stdin is not None:
			self._process.stdin.close()
		
		await self._process.wait()