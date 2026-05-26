"""Seed sample data for demo purposes."""

import asyncio
import os
import sys

import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "../../data/sample")


async def seed():
    sample_files = []
    for f in os.listdir(SAMPLE_DIR):
        path = os.path.join(SAMPLE_DIR, f)
        if os.path.isfile(path) and not f.startswith("."):
            sample_files.append((f, path))

    if not sample_files:
        print("No sample files found.")
        return

    async with httpx.AsyncClient(timeout=120.0) as client:
        for filename, filepath in sample_files:
            print(f"Uploading {filename}...")
            with open(filepath, "rb") as f:
                response = await client.post(
                    f"{BACKEND_URL}/api/upload",
                    files={"file": (filename, f)},
                )

            if response.status_code == 200:
                result = response.json()
                print(f"  OK: {result['document_id'][:8]}... - {result['message']}")
            else:
                print(f"  FAILED: {response.status_code} - {response.text}")

    print(f"\nSeeded {len(sample_files)} sample documents.")


if __name__ == "__main__":
    asyncio.run(seed())
