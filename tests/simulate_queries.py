import requests
import pandas as pd
import time

prompts = [
    # Exact repeats — should HIT after first
    "What is machine learning?",
    "What is machine learning?",
    "What is machine learning?",
    "What is deep learning?",
    "What is deep learning?",
    "What is deep learning?",
    "Explain neural networks",
    "Explain neural networks",
    "What is Python?",
    "What is Python?",
    # Semantic variants — should HIT at 0.90
    "Can you describe what machine learning is?",
    "Define machine learning",
    "Explain machine learning to me",
    "What do you mean by deep learning?",
    "Describe deep learning",
    "What are neural networks?",
    "Tell me about neural networks",
    "What is the Python programming language?",
    "Describe Python as a language",
    # Novel queries — always MISS
    "What is the boiling point of water?",
    "Who wrote Hamlet?",
    "What is the speed of light?",
    "What is photosynthesis?",
    "Who was Albert Einstein?",
    "What is the capital of Japan?",
    "What is DNA?",
    "How does gravity work?",
    "What is blockchain?",
    "What is quantum computing?",
] * 10  # 300 prompts total

results = []
for i, prompt in enumerate(prompts[:300]):
    start = time.time()
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions/sim_session",
            json={"messages": [{"role": "user", "content": prompt}]},
            timeout=60
        )
        data = response.json()
        results.append({
            "query_id": i,
            "prompt": prompt[:50],
            "cache_status": data["cache_status"],
            "latency_ms": data["latency_ms"],
        })
        print(f"[{i+1}/300] {data['cache_status']} — {data['latency_ms']}ms")
    except Exception as e:
        print(f"[{i+1}/300] ERROR — {e}")
    time.sleep(0.1)

df = pd.DataFrame(results)
df.to_csv("tests/simulation_results.csv", index=False)

print(f"\n--- RESULTS ---")
print(f"Cache Hit Rate: {(df['cache_status']=='HIT').mean()*100:.1f}%")
print(f"Avg HIT latency: {df[df['cache_status']=='HIT']['latency_ms'].mean():.1f}ms")
print(f"Avg MISS latency: {df[df['cache_status']=='MISS']['latency_ms'].mean():.1f}ms")