import json
import typing

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
    with open('words.txt') as word_file:
        valid_words = set(word_file.read().split())

    best_score = {"symbols":"", "score":0}
    longest_word = {"symbols":"", "score":0}
    best_ratio = {"symbols":"", "score":0, "ratio":0}
    i = 0
    l = len(valid_words)
    for word in valid_words:
        for result in solve_word(word):
            if result["score"] > best_score["score"]:
                print(f"New best score: {result['symbols']} : {result['score']}")
                best_score = result

            if len(result["symbols"]) > len(longest_word["symbols"]):
                print(f"New longest: {result['symbols']} : {result['score']}")
                longest_word = result

            if result["score"]/len(result["symbols"]) > best_ratio["ratio"]:
                result["ratio"] = result["score"]/len(result["symbols"])
                print(f"Best ratio: {result['symbols']} : {result['score']} : {result['ratio']}")
                best_ratio = result
        i += 1
        if i % 10_000 == 0:
            print(f"{i}/{l}")
    print(f"Best score: {best_score}")
    print(f"Longest word: {longest_word}")
    print(f"Best ratio: {best_ratio}")
    print("Done.")