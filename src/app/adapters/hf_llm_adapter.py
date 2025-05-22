"""
hf_llm_adapter.py

HuggingFace LLM Adapter for Microservices-based FastAPI Applications
--------------------------------------------------------------------

This module provides an adapter class, `HfLLMAdapter`, that integrates HuggingFace's 
transformers library into a microservices-oriented FastAPI application architecture. 
It implements the `LLMPort` interface, enabling seamless, asynchronous interaction with 
a large language model (LLM) for tasks such as text generation or conversational AI.

Usage Context:
- Designed for use in distributed or microservices-based systems where language model 
  interactions should be decoupled via well-defined ports/adapters.
- Accommodates FastAPI's async nature by offloading blocking inference calls to a 
  background thread, ensuring responsive HTTP endpoints.

Core Components:
- `HfLLMAdapter`: An adapter class that receives text prompts and returns generated 
  text using a specified transformer model. It leverages asyncio for concurrency and 
  isolates synchronous model calls from the async event loop.

Example:
    adapter = HfLLMAdapter(model_name="gpt2")
    response = await adapter.chat("What is FastAPI?")

Dependencies:
- transformers
- asyncio

Typical Use in a FastAPI Microservice:
- Instantiate this adapter within a dependency-injected FastAPI "service" layer.
- Call the async `chat` method from FastAPI endpoints to serve LLM-powered responses.

"""

import asyncio
from transformers import pipeline
from app.ports.llm_port import LLMPort

class HfLLMAdapter(LLMPort):
    def __init__(self, model_name: str):
        self.pipe = pipeline("text-generation", model=model_name)

    async def chat(self, prompt: str) -> str:
        loop = asyncio.get_running_loop()
        outputs = await loop.run_in_executor(
            None,
            lambda: self.pipe(prompt, max_length=200)
        )
        return outputs[0]["generated_text"]
