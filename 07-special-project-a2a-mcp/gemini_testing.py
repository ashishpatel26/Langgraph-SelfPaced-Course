from langchain_google_genai import ChatGoogleGenerativeAI
import os

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=os.getenv("GOOGLE_API_KEY"))

model_with_search = model.bind_tools([{"google_search": {}}])
response = model_with_search.invoke("When is the next total solar eclipse in US?")

print(response.content_blocks)