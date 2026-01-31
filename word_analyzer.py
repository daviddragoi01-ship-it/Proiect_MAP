import sys
import re
import json
import csv
from collections import Counter

def load_stopwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(line.strip().lower() for line in f)
    except FileNotFoundError:
        return set()

def clean_text(text):
    # Eliminăm punctuația și convertim în lowercase
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return words

def get_ngrams(words, n):
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

def analyze_text(file_path, stop_words=None, top_n=10, n_gram_size=1):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Eroare la citirea fișierului: {e}")
        return

    all_words = clean_text(content)
    filtered_words = [w for w in all_words if w not in (stop_words or set())]
    
    if n_gram_size > 1:
        tokens = get_ngrams(filtered_words, n_gram_size)
        label = f"Top {top_n} {n_gram_size}-grame"
    else:
        tokens = filtered_words
        label = f"Top {top_n} cuvinte (fără stopwords)"

    count = Counter(tokens)
    total = len(tokens)
    
    print(f"\n{label}:")
    for i, (word, freq) in enumerate(count.most_common(top_n), 1):
        percentage = (freq / total) * 100 if total > 0 else 0
        print(f"{i}. {word:<15} - {freq} apariții ({percentage:.2f}%)")

def show_diversity(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    words = clean_text(content)
    unique_words = set(words)
    ttr = len(unique_words) / len(words) if words else 0
    avg_len = sum(len(w) for w in words) / len(words) if words else 0
    
    print(f"\nDiversitate vocabular:")
    print(f"Total cuvinte: {len(words)}")
    print(f"Cuvinte unice: {len(unique_words)} ({len(unique_words)/len(words)*100:.1f}%)")
    print(f"Type-Token Ratio: {ttr:.3f}")
    print(f"Lungime medie cuvânt: {avg_len:.1f} caractere")

def concordance(file_path, target_word):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\nConcordanță pentru '{target_word}':")
    count = 0
    for line in lines:
        if target_word.lower() in line.lower():
            count += 1
            # Curățăm puțin linia pentru afișare
            clean_line = line.strip()
            highlighted = clean_line.lower().replace(target_word.lower(), f"*{target_word}*")
            print(f"{count}. ...{highlighted}...")

def main():
    # Exemplu de parsare simplă a argumentelor (pentru demo)
    args = sys.argv[1:]
    
    if not args:
        print("Utilizare: python word_analyzer.py <fisier.txt> [--top N] [--diversity] [--ngrams N] [--concordance WORD]")
        return

    file_path = args[0]
    
    # Parametri default
    top_n = 10
    n_gram_size = 1
    stop_words = set(['și', 'de', 'pentru', 'că', 'un', 'o', 'la', 'în', 'pe']) # Stopwords de bază RO

    if "--top" in args:
        top_n = int(args[args.index("--top") + 1])
    
    if "--ngrams" in args:
        n_gram_size = int(args[args.index("--ngrams") + 1])

    if "--diversity" in args:
        show_diversity(file_path)
    elif "--concordance" in args:
        word = args[args.index("--concordance") + 1]
        concordance(file_path, word)
    else:
        analyze_text(file_path, stop_words, top_n, n_gram_size)

if __name__ == "__main__":
    main()