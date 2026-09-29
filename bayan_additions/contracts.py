"""Pure functions extracted from original cells 45, 46, 55; see provenance."""

def align_word_labels(word_ids, word_labels, ignore_index=-100):
    aligned = []
    previous = None
    for word_id in word_ids:
        if word_id is None:
            aligned.append(ignore_index)
        else:
            if word_id < 0 or word_id >= len(word_labels):
                raise ValueError(f"word id out of range: {word_id}")
            aligned.append(word_labels[word_id] if word_id != previous else ignore_index)
        previous = word_id
    return aligned

def bio_entities(tags):
    entities, current_type, start = set(), None, -1
    for index, tag in enumerate(list(tags) + ["O"]):
        if tag == "O":
            if current_type is not None:
                entities.add((current_type, start, index))
            current_type, start = None, -1
            continue
        prefix, entity_type = tag.split("-", 1)
        if prefix == "B" or current_type != entity_type:
            if current_type is not None:
                entities.add((current_type, start, index))
            current_type, start = entity_type, index
    return entities

def entity_report(true_sequences, predicted_sequences):
    gold, predicted = set(), set()
    for sequence_id, (truth, guess) in enumerate(zip(true_sequences, predicted_sequences)):
        gold |= {(sequence_id, *span) for span in bio_entities(truth)}
        predicted |= {(sequence_id, *span) for span in bio_entities(guess)}
    tp, fp, fn = len(gold & predicted), len(predicted - gold), len(gold - predicted)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1,
            "true_entities": len(gold), "predicted_entities": len(predicted)}

def best_span(start_logits, end_logits, offsets, context,
              null_threshold=0.0, max_answer_length=48, top_k=20):
    if not start_logits or len(start_logits) != len(end_logits) or len(offsets) != len(start_logits):
        raise ValueError("logits and offsets must have the same non-zero length")
    null_score = float(start_logits[0]) + float(end_logits[0])
    starts = sorted(range(len(start_logits)), key=lambda i: start_logits[i], reverse=True)[:top_k]
    ends = sorted(range(len(end_logits)), key=lambda i: end_logits[i], reverse=True)[:top_k]
    best = None
    for start in starts:
        for end in ends:
            if start == 0 or end == 0 or end < start or end - start + 1 > max_answer_length:
                continue
            if offsets[start] is None or offsets[end] is None:
                continue
            char_start, char_end = offsets[start][0], offsets[end][1]
            if char_end <= char_start or char_end > len(context):
                continue
            score = float(start_logits[start]) + float(end_logits[end])
            if best is None or score > best["score"]:
                best = {"answer": context[char_start:char_end], "score": score,
                        "start": char_start, "end": char_end}
    if best is None:
        return {"answer": None, "reason": "no_valid_span", "margin": float("inf")}
    margin = null_score - best["score"]
    if margin > null_threshold:
        return {"answer": None, "reason": "no_answer_in_context", "margin": margin}
    return {**best, "null_margin": margin}