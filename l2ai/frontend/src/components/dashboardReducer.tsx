import { createRef, RefObject } from "react";
import { IDashboardState, IDictionaryEntry, IPhrase } from "../interfaces";
import { dummyDefinition } from "../dummyData";
import { scrollToMiddle } from "../utils";

type Action =
  | { type: "EDIT_INPUT"; text: string }
  | { type: "CLICK_START" }
  | { type: "CLICK_BLOCK"; index: number }
  | { type: "CLICK_PHRASE_CARD"; index: number }
  | { type: "CLICK_PHRASE"; index: number }
  | { type: "GET_DICTIONARY_ENTRIES"; index: number; entries: IDictionaryEntry[] }
  | { type: "REMOVE_BLOCK"; index: number };


const reducer = (state: IDashboardState, action: Action) => {
  switch (action.type) {
    case "CLICK_START": {
      if (state.inputText === "") return state;
      const paragraphSplit = state.inputText.split(/\n+/);  // Splits text by paragraphs
      const blockRefs: (RefObject<HTMLSpanElement> | null)[] = [];

      const blocks = paragraphSplit
        .filter((p) => p.trim() !== "")
        .flatMap((p, i) => {
          const words = p.split(" ").flatMap((word, j) => {
            const refWord = createRef<HTMLSpanElement>();
            const refSpace = createRef<HTMLSpanElement>();
            blockRefs.push(refWord, refSpace);

            return [
              <span
                className={"text-block font-l"}
                key={`word-${i}-${j}`}
                ref={refWord}
              >
                {word}
              </span>,
              j < p.split(" ").length - 1 && (
                <span
                  className={"text-block font-l"}
                  key={`space-${i}-${j}`}
                  ref={refSpace}
                >
                  &nbsp;
                </span>
              ),
            ];
          });

          blockRefs.push(null, null);  // Don't include refs for the <br /> elements
          return [...words, <br key={`b1-${i}`} />, <br key={`b2-${i}`} />];
        });

      return { ...state, blocks, blockRefs, showInput: false };
    }
    case "CLICK_BLOCK": {
      const { index } = action;

      // If the user clicks a non-active block
      if (
        !state.selectedIndices.includes(index)
        && state.blockRefs?.[index]?.current
      ) {
        const blockRef = state.blockRefs[index];
        const block = state.blockRefs[index]?.current;

        if (block && blockRef) {
          const updatedSelectedIndices = [...state.selectedIndices, index];
          const updatedPhrases = [...state.phrases];
          updatedPhrases.forEach(phrase => phrase.active = false);

          // Mark the block as active with an underline
          block.classList.add("text-block-0");

          // Always create a new phrase on each click
          const newPhrase: IPhrase = {
            active: true,
            startIndex: index,
            stopIndex: index,
            refs: [blockRef],
            dictionaryEntries: null,
            explanation: ""
          };

          // Check for an adjacent block to the left
          if (state.selectedIndices.includes(index - 2)) {

            // Get the phrase that contains the adjacent block
            const leftPhraseIx = updatedPhrases.findIndex(
              phrase => phrase.stopIndex == index - 2
            );

            // If the adjacent block is not the end of a sentence
            if (!block.innerHTML.endsWith(".")) {

              // Merge the adjacent phrase with the new phrase
              // TODO: handle when the adjacent phrase has an explanation
              newPhrase.startIndex = updatedPhrases[leftPhraseIx].startIndex;
              newPhrase.refs = [
                ...updatedPhrases[leftPhraseIx].refs,
                ...newPhrase.refs
              ];

              // Delete the adjacent phrase
              updatedPhrases.splice(leftPhraseIx, 1);

              // Underline the span containing "&nbsp;" between the two blocks
              const spaceElement = state.blockRefs[index - 1]?.current;
              spaceElement?.classList.add("text-block-0");
            }
          }

          // Check for an adjacent block to the right as before
          if (state.selectedIndices.includes(index + 2)) {
            const rightPhraseIx = updatedPhrases.findIndex(
              phrase => phrase.startIndex == index + 2
            );
            if (
              !(block.innerHTML.endsWith(".")
              || updatedPhrases[rightPhraseIx].explanation !== ""))
            {
              newPhrase.stopIndex = updatedPhrases[rightPhraseIx].stopIndex;
              newPhrase.refs = [
                ...newPhrase.refs,
                ...updatedPhrases[rightPhraseIx].refs
              ];
              updatedPhrases.splice(rightPhraseIx, 1);
              const spaceElement = state.blockRefs[index + 1]?.current;
              spaceElement?.classList.add("text-block-0");
            }
          }

          updatedPhrases.push(newPhrase);
          updatedPhrases.sort((a, b) => {
            if (a.startIndex > b.startIndex) return 1;
            else if (a.startIndex < b.startIndex) return -1;
            return 0;
          });

          return {
            ...state,
            selectedIndices: updatedSelectedIndices,
            phrases: updatedPhrases
          };
        }
      }
      return state;
    }
    case "CLICK_PHRASE_CARD": {
      const { index } = action;
      const updatedPhrases = [...state.phrases];

      // Get the container's dimensions and scroll position
      const container = updatedPhrases[index].refs[0].current?.parentElement;
      const element = updatedPhrases[index].refs[0].current;
      if (container && element) scrollToMiddle(container, element);

      updatedPhrases.forEach((phrase, i) => phrase.active = index == i);
      return { ...state, phrases: updatedPhrases };
    }
    case "CLICK_PHRASE": {
      const { index } = action;
      const updatedPhrases = [...state.phrases];
      updatedPhrases.forEach((phrase, i) => phrase.active = index == i);
      return { ...state, phrases: updatedPhrases };
    }
    case "GET_DICTIONARY_ENTRIES": {
      const { index, entries } = action;
      const updatedPhrases = [...state.phrases];
      updatedPhrases[index].dictionaryEntries = entries;
      return { ...state, phrases: updatedPhrases };
    }
    case "REMOVE_BLOCK": {
      const { index } = action;

      if (state.blockRefs?.[index]?.current) {  // TODO: require that phrase must be selected first
        const blockRef = state.blockRefs[index];
        const block = state.blockRefs[index]?.current;

        if (block && blockRef) {
          const updatedSelectedIndices = [...state.selectedIndices];
          const updatedPhrases = [...state.phrases];

          // Remove the index from selectedIndices
          const foundIx = state.selectedIndices.findIndex(ix => ix == index);
          updatedSelectedIndices.splice(foundIx, 1);

          // Mark the block as inactive by removing the underline
          block.classList.remove("text-block-0");

          // Check for adjacent words and remove any underlined whitespace
          if (state.selectedIndices.includes(index - 2)) {
            const spaceElement = state.blockRefs[index - 1]?.current;
            spaceElement?.classList.remove("text-block-0");
          }

          if (state.selectedIndices.includes(index + 2)) {
            const spaceElement = state.blockRefs[index + 1]?.current;
            spaceElement?.classList.remove("text-block-0");
          }

          // Find the phrase that contains current block
          const phraseIx = updatedPhrases.findIndex(
            phrase => phrase.startIndex <= index && index <= phrase.stopIndex
          );
          const phrase = updatedPhrases[phraseIx];

          // Split the phrase into one or two new phrases that don't contain the block
          const newPhrases: IPhrase[] = [];
          if (phrase.startIndex < index) {
            newPhrases.push({
              active: true,
              startIndex: phrase.startIndex,
              stopIndex: index - 2,
              refs: phrase.refs.slice(0, (index - phrase.startIndex) / 2),
              dictionaryEntries: null,
              explanation: "" });
          }
          if (index < phrase.stopIndex) {
            newPhrases.push({
              active: false,
              startIndex: index + 2,
              stopIndex: phrase.stopIndex,
              refs: phrase.refs.slice((index + 2 - phrase.startIndex) / 2),
              dictionaryEntries: null,
              explanation: "" });
          }

          // Remove and replace the previous phrase
          updatedPhrases.splice(phraseIx, 1);
          updatedPhrases.push(...newPhrases);

          return {
            ...state,
            selectedIndices: updatedSelectedIndices,
            phrases: updatedPhrases
          };
        }
      }
      return state;
    }
    default:
      return state;
  }
};


export default reducer;
