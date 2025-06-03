import asyncio
import httpx
import json
from typing import Dict, Any, Optional, List

BASE_URL = "http://localhost:8000/api/v1"

async def test_drill_group_api():
    """Test the drill group API endpoints"""
    # Get all drill groups
    print("\n1. Testing GET /drill-groups/ - List all drill groups")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/drill-groups/")
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            drill_groups = response.json()
            print(f"Found {len(drill_groups)} drill groups")
        else:
            print(f"Error: {response.text}")
    
    # Create a drill group
    print("\n2. Testing POST /drill-groups/ - Create a drill group")
    drill_group_data = {
        "name": "Test Drill Group",
        "description": "Test description",
        "is_public": True,
        "difficulty": 2,
        "tags": ["test", "api"],
        "drill_ids": []  # We'll add drills later
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/drill-groups/", json=drill_group_data)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            new_group = response.json()
            print(f"Created drill group with ID: {new_group['id']}")
            drill_group_id = new_group["id"]
        else:
            print(f"Error: {response.text}")
            return
      # Get available drills to add to the group
    print("\n3. Testing GET /drill/ - List available drills")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/drill/")
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            drills = response.json()
            print(f"Found {len(drills)} drills")
            if drills:
                drill_ids = [drill["id"] for drill in drills[:2]]  # Get first 2 drills
                print(f"Selected drill IDs: {drill_ids}")
            else:
                drill_ids = []
        else:
            print(f"Error: {response.text}")
            drill_ids = []
    
    # Add drills to the group
    if drill_ids:
        print("\n4. Testing PUT /drill-groups/{id}/drills - Update drills")
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{BASE_URL}/drill-groups/{drill_group_id}/drills", params={"drill_ids": drill_ids})
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                updated_group = response.json()
                print(f"Updated drill group with drills: {[d['id'] for d in updated_group.get('drills', [])]}")
            else:
                print(f"Error: {response.text}")
    
    # Get the specific drill group
    print(f"\n5. Testing GET /drill-groups/{drill_group_id} - Get specific drill group")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/drill-groups/{drill_group_id}")
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            drill_group = response.json()
            print(f"Drill group name: {drill_group['name']}")
            print(f"Drill group has {len(drill_group.get('drills', []))} drills")
        else:
            print(f"Error: {response.text}")
    
    print("\nDrill Group API Test completed!")

if __name__ == "__main__":
    asyncio.run(test_drill_group_api())
