import asyncio
from ollama import AsyncClient
import websockets
import json

async def handle_message(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            user_message = data['message']
            model = data.get('model', 'phi3')  # Default to 'llama2' if not provided

            client = AsyncClient(host='http://localhost:11434')
            response = await client.chat(model=model, messages=[{'role': 'user', 'content': user_message}])
            ollama_response = response['message']['content']

            await websocket.send(json.dumps({'response': ollama_response}))
        except Exception as e:
            print(f"Error: {e}")
            await websocket.send(json.dumps({'error': str(e)}))

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("Ollama bot server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())