import asyncio
import httpx
import time

# The URL of your running API
API_URL = "http://127.0.0.1:8000/generate"

# Topics for the concurrent requests. Using different topics avoids hitting the cache.
TOPICS = [
    "The History of Ancient Rome",
    "The Future of Renewable Energy",
    "An Introduction to Quantum Computing",
]

async def make_request(client: httpx.AsyncClient, topic: str):
    """Sends a single request and prints the time taken."""
    print(f"-> Starting request for: '{topic}'")
    payload = {"topic": topic, "num_slides": 15}
    start_time = time.time()

    try:
        # Set a long timeout because the API call can be slow
        response = await client.post(API_URL, json=payload, timeout=120.0)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        end_time = time.time()
        duration = end_time - start_time
        print(f"<- Finished request for: '{topic}' in {duration:.2f} seconds.")
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] Request failed for '{topic}': {e.response.status_code} {e.response.text}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred for '{topic}': {e}")


async def main():
    """Runs all requests concurrently and measures total time."""
    print("--- Starting Concurrency Test ---")
    total_start_time = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, topic) for topic in TOPICS]
        await asyncio.gather(*tasks)

    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    print(f"\n--- Test Finished ---")
    print(f"Total time to complete {len(TOPICS)} concurrent requests: {total_duration:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())

"""
--- Starting Concurrency Test ---
-> Starting request for: 'The History of Ancient Rome'
-> Starting request for: 'The Future of Renewable Energy'
-> Starting request for: 'An Introduction to Quantum Computing'
<- Finished request for: 'An Introduction to Quantum Computing' in 6.97 seconds.
<- Finished request for: 'The Future of Renewable Energy' in 7.83 seconds.
<- Finished request for: 'The History of Ancient Rome' in 9.79 seconds.

--- Test Finished ---
Total time to complete 3 concurrent requests: 9.85 seconds.
"""


