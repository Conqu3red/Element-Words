import json
import typing
import sys
from reprint import output

with open("elements.json", "rb") as f:
    data = json.load(f)

def solve_word(word: str, offset: int = 0, score = 0, tmp_str = "", matches: list = None):
    if matches == None:
        matches = []
    if offset == len(word):
        matches.append({"symbols":tmp_str, "score":score})
        #print(f"{tmp_str} : {score}")
    for element in data["elements"]:
        if word[offset:offset+len(element["symbol"])] == element["symbol"].lower():
            #print(f"match: {element['symbol']}")
            solve_word(
                word, 
                offset=offset + len(element["symbol"]), 
                score=score+round(element["atomic_mass"]), 
                tmp_str=tmp_str+element["symbol"], 
                matches=matches
            )
    return matches

def solve_sentence(sentence: str):
    result = {"symbols": "", "score": 0}
    for word in sentence.split():
        results = solve_word(word)
        if len(results) == 0:
            return None
        best = sorted(results, key=lambda r: r["score"], reverse=True)[0]
        result["symbols"] += " " + best["symbols"]
        result["score"] += best["score"]
    return result

if __name__ == "__main__":
    with output(output_type='dict') as output_lines:
        with open('words.txt') as word_file:
            valid_words = word_file.read().split()

        best_score = {"symbols":"", "score":0}
        longest_word = {"symbols":"", "score":0}
        best_ratio = {"symbols":"", "score":0, "ratio":0}
        amazing_words = []
        best_word_at_length = {}

        i = 0
        l = len(valid_words)

        def rewrite_progress():  
            output_lines["Progress"] = f"{int((i/l)*100)}% ({i}/{l})"
            output_lines["Best Score"] = f"{best_score['symbols']} score: {best_score['score']}"
            output_lines["Longest Word"] = f"{longest_word['symbols']} score: {longest_word['score']} length: {len(longest_word['symbols'])}"
            #output_lines["Good words"] = ", ".join([f"{w['symbols']} ({w['score']})" for w in amazing_words])
        for word in valid_words:
            best = {"score":0}
            for result in solve_word(word):
                if result["score"] > best_score["score"]:
                    rewrite_progress()
                    best_score = result

                if len(result["symbols"]) > len(longest_word["symbols"]):
                    rewrite_progress()
                    longest_word = result

                if result["score"]/len(result["symbols"]) > best_ratio["ratio"]:
                    result["ratio"] = result["score"]/len(result["symbols"])
                    rewrite_progress()
                    best_ratio = result
                if result["score"] > best["score"]:
                    best = result
                if not best_word_at_length.get(len(result["symbols"])) or result["score"] > best_word_at_length.get(len(result["symbols"]))["score"]:
                    best_word_at_length[len(result["symbols"])] = result
            if best and best["score"] > 1500:
                amazing_words.append(best)
            i += 1
            if i % 10_000 == 0:
                rewrite_progress()
        rewrite_progress()
    print("Done.")

    print("Best word at every length:")
    for k, w in {k:v for k,v in sorted(best_word_at_length.items())}.items():
        print(f"  {k} - {w['symbols'].lower()} - {w['symbols']} ({w['score']})")
    print("Words that score above 1500:")
    for w in amazing_words:
        print(f"  {w['symbols'].lower()} - {w['symbols']} ({w['score']})")
        