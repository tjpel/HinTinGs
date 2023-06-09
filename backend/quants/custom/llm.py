from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Union,
)
import openai

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from langchain.llms.openai import BaseOpenAI, OpenAIChat
from langchain.schema import Generation, LLMResult
import logging

logger = logging.getLogger(__name__)

def _create_retry_decorator(llm: Union[BaseOpenAI, OpenAIChat]) -> Callable[[Any], Any]:
    import openai

    min_seconds = 4
    max_seconds = 10
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(llm.max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(openai.error.Timeout)
            | retry_if_exception_type(openai.error.APIError)
            | retry_if_exception_type(openai.error.APIConnectionError)
            | retry_if_exception_type(openai.error.RateLimitError)
            | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )

def completion_with_retry(llm: Union[BaseOpenAI, OpenAIChat], **kwargs: Any) -> Any:
    """Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(llm)

    @retry_decorator
    def _completion_with_retry(**kwargs: Any) -> Any:
        return openai.ChatCompletion.create(**kwargs)

    return _completion_with_retry(**kwargs)

def update_token_usage(
    keys: Set[str], response: Dict[str, Any], token_usage: Dict[str, Any]
) -> None:
    """Update token usage."""
    _keys_to_use = keys.intersection(response["usage"])
    for _key in _keys_to_use:
        if _key not in token_usage:
            token_usage[_key] = response["usage"][_key]
        else:
            token_usage[_key] += response["usage"][_key]


class CustomOpenAI(BaseOpenAI):
    """Generic OpenAI class that uses model name."""

    @property
    def _invocation_params(self) -> Dict[str, Any]:
        return {**{"model": self.model_name}, **super()._invocation_params}

    def __new__(cls, **data: Any) -> Union[OpenAIChat, BaseOpenAI]:  # type: ignore
        """Initialize the OpenAI object."""
        return super().__new__(cls)
    

    def _generate(
        self, prompts: List[str], stop: Optional[List[str]] = None
    ) -> LLMResult:
        """Call out to OpenAI's endpoint with k unique prompts.
        Args:
            prompts: The prompts to pass into the model.
            stop: Optional list of stop words to use when generating.
        Returns:
            The full LLM output.
        Example:
            .. code-block:: python
                response = openai.generate(["Tell me a joke."])
        """
        # TODO: write a unit test for this
        params = self._invocation_params
        # print(params)
        params.pop('best_of', None)
        sub_prompts = self.get_sub_prompts(params, prompts, stop)
        choices = []
        token_usage: Dict[str, int] = {}
        # Get the token usage from the response.
        # Includes prompt, completion, and total tokens used.
        _keys = {"completion_tokens", "prompt_tokens", "total_tokens"}
        for _prompts in sub_prompts:
            for p in _prompts:
                print('PROMPT:\n', p[:100], '\n\n')
                response = completion_with_retry(
                    self, 
                    messages=[
                        { 'role': 'system', 'content': 'you are a helpful assistant. Only use the sources provided. Do not use outside information or guess answers.' },
                        { 'role': 'user', 'content': p }
                    ], 
                    **params
                )
                choices.extend(response["choices"])
                update_token_usage(_keys, response, token_usage)
        return self.create_llm_result(choices, prompts, token_usage)

    def create_llm_result(
        self, choices: Any, prompts: List[str], token_usage: Dict[str, int]
    ) -> LLMResult:
        """Create the LLMResult from the choices and prompts."""
        generations = []
        for i, _ in enumerate(prompts):
            sub_choices = choices[i * self.n : (i + 1) * self.n]
            generations.append(
                [
                    Generation(
                        text=choice.message.content,
                        generation_info=dict(
                            finish_reason=choice.get("finish_reason"),
                            logprobs=choice.get("logprobs"),
                        ),
                    )
                    for choice in sub_choices
                ]
            )
        return LLMResult(
            generations=generations, llm_output={"token_usage": token_usage}
        )