from app.cache.semantic_cache import SemanticCache

similar_pairs = [
    ("What is machine learning?", "Explain machine learning to me"),
    ("What is machine learning?", "Can you describe what machine learning is?"),
    ("What is machine learning?", "Define machine learning"),
    ("How do I reset my password?", "What are the steps to change my password?"),
    ("What is the capital of France?", "Tell me the capital city of France"),
]

thresholds = [0.85, 0.88, 0.90, 0.92, 0.95]

print(f"\n{'Threshold':<12} {'Hits':<8} {'Total':<8} {'Hit Rate'}")
print("-" * 40)

for threshold in thresholds:
    test_cache = SemanticCache(threshold=threshold)
    hits = 0

    for q1, q2 in similar_pairs:
        test_cache.set(q1, "cached response")
        result = test_cache.get(q2)
        if result:
            hits += 1

    print(f"{threshold:<12} {hits:<8} {len(similar_pairs):<8} {hits/len(similar_pairs)*100:.0f}%")