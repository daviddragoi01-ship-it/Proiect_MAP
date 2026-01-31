import sys
import re
import json
import csv
from collections import Counter

# 1. STOPWORDS & FILTRARE
STOPWORDS_RO = {'și', 'de', 'pentru', 'că', 'un', 'o', 'la', 'în', 'pe', 'cu', 'din', 'să', 'este'}
STOPWORDS_EN = {'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'for', 'on'}

def clean_text(text):
    # TOKENIZARE ȘI NORMALIZARE
    text = text.lower()
    return re.findall(r'\b\w+\b', text)

def get_stats(words):
    # LUNGIME MEDIE ȘI DIVERSITATE
    if not words: return 0, 0, 0
    unique = set(words)
    avg_len = sum(len(w) for w in words) / len(words)
    ttr = len(unique) / len(words) # Type-Token Ratio
    return avg_len, len(unique), ttr

def generate_word_cloud_text(counter, limit=15):
    # GENERARE WORD CLOUD (TEXT)
    print("\n--- WORD CLOUD (TEXT) ---")
    max_freq = counter.most_common(1)[0][1] if counter else 1
    for word, freq in counter.most_common(limit):
        size = int((freq / max_freq) * 10) + 1
        print(f"{word.upper() if size > 5 else word} {'*' * size}")

def run_analysis(file_path, n_gram=1, top_n=10, export=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    all_words = clean_text(text)
    # FILTRARE STOPWORDS
    filtered = [w for w in all_words if w not in STOPWORDS_RO and w not in STOPWORDS_EN]
    
    # N-GRAMS (BIGRAME, TRIGRAME)
    if n_gram > 1:
        tokens = [" ".join(all_words[i:i+n_gram]) for i in range(len(all_words)-n_gram+1)]
    else:
        tokens = filtered

    counts = Counter(tokens)
    top_results = counts.most_common(top_n)
    
    # AFIȘARE REZULTATE
    print(f"\nAnaliză: {file_path} ({len(all_words)} cuvinte)")
    for i, (item, freq) in enumerate(top_results, 1):
        print(f"{i}. {item}: {freq}")

    # EXPORT JSON/CSV
    if export == 'json':
        with open('results.json', 'w') as f: json.dump(dict(top_results), f)
    elif export == 'csv':
        with open('results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(top_results)

    return all_words, counts

def compare_docs(file1, file2):
    # COMPARAȚIE ÎNTRE DOCUMENTE
    words1 = set(clean_text(open(file1, 'r', encoding='utf-8').read()))
    words2 = set(clean_text(open(file2, 'r', encoding='utf-8').read()))
    common = words1.intersection(words2)
    print(f"\nComparație: {len(common)} cuvinte comune între fișiere.")

def search_concordance(file_path, keyword):
    # CĂUTARE CONTEXT (CONCORDANȚĂ)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    matches = re.findall(r'(.{0,30}' + re.escape(keyword.lower()) + r'.{0,30})', content)
    print(f"\nConcordanță pentru '{keyword}':")
    for m in matches[:5]: print(f"...{m}...")

def main():
    args = sys.argv[1:]
    if not args: return
    
    f1 = args[0]
    
    if "--compare" in args:
        compare_docs(f1, args[args.index("--compare") + 1])
    elif "--concordance" in args:
        search_concordance(f1, args[args.index("--concordance") + 1])
    elif "--diversity" in args:
        w = clean_text(open(f1, 'r', encoding='utf-8').read())
        avg, uniq, ttr = get_stats(w)
        print(f"Diversitate: {ttr:.3f}, Lungime medie: {avg:.2f}")
    else:
        # Implicit: Top frecvență și Word Cloud
        words, counts = run_analysis(f1)
        generate_word_cloud_text(counts)

if __name__ == "__main__":
    main()
