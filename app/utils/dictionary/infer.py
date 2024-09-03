import re

import jamotools
import torch
from transformers import AutoTokenizer, AutoModelForMultipleChoice

from app.collections import DictionaryEntryWithSenses
from app.utils.dictionary.dictionary import query_dictionary

# Initialize the model and tokenizer
model_name = "JesseStover/L2AI-dictionary-klue-bert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMultipleChoice.from_pretrained(model_name)
model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

# Single common words to exclude from inference
exclude_words = ["것", "수", "있다", "안", "하다", "되다"]


def ends_in_vowel(str: str) -> bool:
    """
    Determine whether a string of Hangul ends in a vowel. Always returns False
    if the string does not end in Hangul.

    Args:
        str (str)

    Returns:
        bool
    """
    char = str[-1]

    if not jamotools.is_syllable(char):
        return False

    jamos = jamotools.split_syllable_char(char)
    return ord(jamos[-1]) >= 0x1161 and ord(jamos[-1]) <= 0x1175


def get_inference(
        query: str,
        context: str | None = None
    ) -> list[DictionaryEntryWithSenses]:
    """
    Analyzes the given query sentence and infers the most probable meanings
    (senses) of each word based on the context.

    The function processes the query by segmenting it into individual words and 
    phrases, retrieving possible definitions for each, and then inferring the 
    most likely definition from the context of the sentence. For instance, given
    "강아지는 뽀송뽀송하다." ("The puppy is fluffy.") it would infer that 
    "강아지" means "puppy" and "뽀송뽀송" means "fluffy".

    Args:
        query (str): The input sentence for which word definitions need to be
            inferred.
        context (str | None, optional): Additional context that might help to 
            disambiguate the definitions. Default is None.

    Returns:
        list[DictionaryEntryWithSenses]: A list of dictionary entries, each
            mapped to its inferred senses with their respective ranks based on 
            the context. Each entry in the list contains the word, its part of 
            speech, and a ranked list of possible meanings.

    Raises:
        ValueError: If a variation in the query string is not found among the 
            dictionary keys searched, indicating a probable issue with the 
            function's internal dictionary lookup.
    """

    # Get all words, idioms, or proverbs in the query
    groups = query_dictionary(query, context)
    result = []

    for group in groups:

        # All words in a group have the same written form, so use the first
        written_form = group[0]["writtenForm"]
        pos = group[0]["partOfSpeech"]  # TODO: use part of speech to improve results

        # If the word is a common excluded word
        if written_form in exclude_words:
            continue

        # Construct the prompt using the variation that was used in the query
        prompt = "\"%s\"에 있는 \"%s\"의 정의는 " % (context, written_form)

        # Construct a list of candidate responses using each of the word's senses
        definitions = []
        for entry in group:
            definitions.extend([sense["definition"] for sense in entry["senses"]])

        # If the word has only one sense
        if len(definitions) == 1:
            infer_result = [1.0]

        else:
            candidates = []

            # Prepare the candidate responses
            for definition in definitions:

                # Remove ending punctuation
                if definition.endswith("."):
                    definition = definition[:-1]

                # Remove all characters that are not Hangul, alphanumeric, or numbers
                definition_stripped = re.sub(
                    r"[^\u3131-\uD79DA-Za-z\d]", "", definition
                )

                # Conjugate the end of the sentence
                end = "예요." if ends_in_vowel(definition_stripped) else "이에요."

                candidates.append("\"%s\"%s" % (definition, end))

            # Prepare the model's inputs
            inputs = tokenizer(
                [[prompt, candidate] for candidate in candidates],
                return_tensors="pt",
                padding=True
            )

            labels = torch.tensor(0).unsqueeze(0)

            # Run the inference
            with torch.no_grad():
                outputs = model(
                    **{k: v.unsqueeze(0) for k, v in inputs.items()},
                    labels=labels
                )

            # Use Softmax to get the inference results
            infer_result = [float(x) for x in outputs.logits.softmax(1)[0]]

        start = 0
        ranks = []

        for entry in group:

            # Get the end index of this word's results
            end = start + len(entry["senses"])

            # Map the results to each sense of this word
            entry["ranks"] = infer_result[start:end]

            # Set the start index of the next word's results
            start = end

            # Make a list of each sense and their scores
            ranks.extend(list(zip(
                [sense["_id"] for sense in entry["senses"]], entry["ranks"]
            )))

        # Sort this word's senses according to its rank
        ranks.sort(key=lambda x: x[1], reverse=True)
        rank_map = dict(ranks)

        # Get dictionary entry that has sense with highest score
        for entry in group:
            for sense in entry["senses"]:
                if sense["_id"] == ranks[0][0]:
                    break

        # Add the rank to each sense
        for sense in entry["senses"]:
            sense["rank"] = rank_map[sense["_id"]]

        result.append(entry)

    return result
