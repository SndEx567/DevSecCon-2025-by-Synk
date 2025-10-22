import requests
import time

# The CORRECT OWASP Top 10 for LLMs list for this specific challenge
correct_order = [
    "Prompt Injection",
    "Sensitive Information Disclosure",
    "Supply Chain",
    "Data and Model Poisoning",
    "Improper Output Handling",
    "Excessive Agency",
    "System Prompt Leakage",
    "Vector and Embedding Weaknesses",
    "Misinformation",
    "Unbounded Consumption"
]

# API endpoints
base_url = "https://challenge.devseccon.com"
get_url = f"{base_url}/api/challenge"
post_url = get_url

def main():
    start_time = time.time()
    print("Attempting to get challenge data...")
    try:
        response = requests.get(get_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"GET request failed: {e}")
        return

    data = response.json()
    shuffled_items = data.get("items", [])

    # Manually set your token here (replace this string with your actual token)
    token =  data.get("token")

    if not shuffled_items or not token:
        print("Error: Could not retrieve items or token from API response.")
        return

    print("Shuffled items from API:")
    for i, item in enumerate(shuffled_items):
        print(f" - [{i}] {item}")

    # Build orderedList: for each item in correct_order, find its index in shuffled_items
    ordered_list = []
    found_all = True
    for item in correct_order:
        try:
            index = shuffled_items.index(item)
            ordered_list.append(index)
        except ValueError:
            print(f"🛑 Critical Error: Item not found in shuffled list: '{item}'. Check your 'correct_order' list.")
            found_all = False
            break

    if not found_all:
        return

    print(f"\n✅ Constructed ordered list of indices: {ordered_list}")

    payload = {
        "orderedList": ordered_list,
        "token": token
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Attempting to submit the ordered list...")

    try:
        response = requests.post(post_url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("POST request failed.")
        print(f"Server response (if available): {getattr(response, 'text', 'N/A')}")
        print(f"Request error: {e}")
        return

    try:
        result = response.json()
    except ValueError:
        print("Error: Server response is not valid JSON.")
        print(f"Raw response: {response.text}")
        return

    elapsed = time.time() - start_time

    print("\n" + "="*40)
    print("✨ CHALLENGE RESULT ✨")
    print("="*40)
    print(f"✅ Success: {result.get('success')}")
    print(f"⏱️ Elapsed Time: {elapsed:.2f} seconds")
    print(f"📦 Completion ID: {result.get('completionId', 'N/A')}")

    messages = result.get("messages", [])
    if messages:
        print("📩 Messages:")
        for msg in messages:
            print(f" - {msg}")

    if result.get('success') == True:
        print("\n🎉 Congratulations! You successfully reordered the list.")
    else:
        print("\n❌ Submission failed. Check the messages for details.")

if __name__ == "__main__":
    main()

