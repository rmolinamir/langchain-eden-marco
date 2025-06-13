from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult


class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> None:
        print(f"***Prompt to LLM was:***\n\n{prompts[0]}")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        print(f"***LLM Response:***\n\n{response.generations[0][0].text}")
