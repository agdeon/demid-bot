from src.services.gpt_service.gpt_api import GPTApiService

response_str = GPTApiService().request([{"role": "system", "content": "Your instruction for gpt"}])
print(response_str)