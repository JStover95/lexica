from functools import reduce
import re
from typing import Tuple
import jamotools
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForMultipleChoice

from l2ai.collections import senses
from l2ai.utils.dictionary.dictionary import query_dictionary, get_query_str
from l2ai.utils.logging import logger

# initialize the model and tokenizer
model_name = "JesseStover/L2AI-dictionary-klue-bert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMultipleChoice.from_pretrained(model_name)
model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

type InferenceResult = dict[str, list[Tuple[float, str]]]

# single common words to exclude from inference
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


def get_inference(query: str) -> InferenceResult:
    """
    Gets each word of a given query then infers the best definitions (senses)
    for each word. For example, the word "강아지" can mean "puppy" or "baby,
    sweetheart." Calling get_inference("강아지는 뽀송뽀송하다.") will:

    1. Break down the query into its constituent words (강아지 and 뽀송뽀송).
    2. Get the senses of each word.
    3. Based on the context of the sentence, infer a score for each sense that
       represents the probability that that is the proper definition.

    In this case, 뽀송뽀송 when used to describe 강아지 means "fuzzily, downily,"
    while 강아지 means "puppy." The inference should return high scores for
    these definitions.

    Args:
        query (str)

    Raises:
        ValueError: When a variation used in the query string is not found in
            one of the query keys used to search the dictionary. This would
            likely be an issue with the function itself and not the query.

    Returns:
        InferenceResult
    """

    # get all words, idioms, or proverbs in the query
    groups = query_dictionary(query)
    result = {}

    for group in tqdm(groups):

        # all words in a group have the same written form, so use the first
        written_form = group[0]["writtenForm"]
        pos = group[0]["partOfSpeech"]

        # if the word is a common excluded word
        if written_form in exclude_words:
            continue

        # construct the prompt using the variation that was used in the query
        prompt = "\"%s\"에 있는 \"%s\"의 정의는 " % (query, written_form)

        # construct a list of candidate responses using each of the word's
        # senses
        definitions = []
        for entry in group:
            definitions.extend([sense["definition"] for sense in entry["senses"]])

        # if the word has only one sense
        if len(definitions) == 1:
            infer_result = [1.0]

        else:
            candidates = []

            # prepare the candidate responses
            for definition in definitions:

                # remove ending punctuation
                if definition.endswith("."):
                    definition = definition[:-1]

                # remove all characters that are not Hangul, alphanumeric, or
                # numbers
                definition_stripped = re.sub(r"[^\u3131-\uD79DA-Za-z\d]", "", definition)

                # conjugate the end of the sentence
                end = "예요." if ends_in_vowel(definition_stripped) else "이에요."

                candidates.append("\"%s\"%s" % (definition, end))

            # prepare the model's inputs
            inputs = tokenizer(
                [[prompt, candidate] for candidate in candidates],
                return_tensors="pt",
                padding=True
            )

            labels = torch.tensor(0).unsqueeze(0)

            # run inference
            with torch.no_grad():
                outputs = model(
                    **{k: v.unsqueeze(0) for k, v in inputs.items()},
                    labels=labels
                )

            # use Softmax to get the inference results
            infer_result = [float(x) for x in outputs.logits.softmax(1)[0]]

        start = 0
        ranks = []

        for entry in group:

            # get the end index of this word's results
            end = start + len(entry["senses"])

            # map the results to each sense of this word
            entry["ranks"] = infer_result[start:end]

            # set the start index of the next word's results
            start = end

            # make a list of each sense and their scores
            ranks.extend(list(zip(entry["ranks"], [sense["definition"] for sense in entry["senses"]])))

        # sort this word's senses according to its rank
        ranks.sort(key=lambda x: x[0], reverse=True)
        result[written_form] = ranks

    return result
