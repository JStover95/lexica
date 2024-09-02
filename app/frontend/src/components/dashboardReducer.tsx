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
  | { type: "CLICK_SEE_MORE_DEFINITIONS"; phraseIx: number; entryIx: number }
  | { type: "CLICK_STAR_BUTTON"; phraseIx: number; entryIx: number; senseIx: number; }
  | { type: "GET_DICTIONARY_ENTRIES"; index: number; entries: IDictionaryEntry[] }
  | { type: "DELETE_PHRASE"; index: number };


const reducer = (state: IDashboardState, action: Action) => {
  switch (action.type) {
    case "EDIT_INPUT": {
      const { text } = action;
      return { ...state, inputText: text };
    }
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
            if (!state.blockRefs[index - 2]?.current?.innerHTML.endsWith(".")) {

              // Underline the span containing "&nbsp;" between the two blocks
              const spaceRef = state.blockRefs[index - 1];
              const spaceElement = spaceRef?.current;
              spaceElement?.classList.add("text-block-0");

              // Merge the adjacent phrase with the new phrase
              // TODO: handle when the adjacent phrase has an explanation
              newPhrase.startIndex = updatedPhrases[leftPhraseIx].startIndex;
              newPhrase.refs = [
                ...updatedPhrases[leftPhraseIx].refs,
                ...(spaceRef ? [spaceRef] : []),
                ...newPhrase.refs
              ];

              // Delete the adjacent phrase
              updatedPhrases.splice(leftPhraseIx, 1);
            }
          }

          // Check for an adjacent block to the right as before
          if (state.selectedIndices.includes(index + 2)) {
            const rightPhraseIx = updatedPhrases.findIndex(
              phrase => phrase.startIndex == index + 2
            );
            if (!state.blockRefs[index + 2]?.current?.innerHTML.endsWith(".")) {
              const spaceRef = state.blockRefs[index + 1];
              const spaceElement = spaceRef?.current;
              spaceElement?.classList.add("text-block-0");
              newPhrase.stopIndex = updatedPhrases[rightPhraseIx].stopIndex;
              newPhrase.refs = [
                ...newPhrase.refs,
                ...(spaceRef ? [spaceRef] : []),
                ...updatedPhrases[rightPhraseIx].refs
              ];
              updatedPhrases.splice(rightPhraseIx, 1);
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
    case "CLICK_SEE_MORE_DEFINITIONS": {
      const { phraseIx, entryIx } = action;
      const updatedPhrases = [...state.phrases];
      const phrase = updatedPhrases[phraseIx];
      if (phrase.dictionaryEntries) {
        const entry = phrase.dictionaryEntries[entryIx].showAll = true;
      }
      return { ...state, phrases: updatedPhrases };
    }
    case "CLICK_STAR_BUTTON": {  // TODO: fix type of action
      const { phraseIx, entryIx, senseIx } = action;
      const updatedPhrases = [...state.phrases];
      const phrase = updatedPhrases[phraseIx];
      if (phrase.dictionaryEntries) {
        const entry = phrase.dictionaryEntries[entryIx];
        entry.showAll = false;
        entry.senses.forEach(sense => {
          if (sense.rank === 1.0) sense.rank = 0.0;
        });
        entry.senses[senseIx].rank = 1.0;
      }
      return { ...state, phrases: updatedPhrases };
    }
    case "GET_DICTIONARY_ENTRIES": {
      const { index, entries } = action;
      const updatedPhrases = [...state.phrases];
      const phrase = updatedPhrases[index];
      if (phrase) {
        updatedPhrases[index].dictionaryEntries = entries;
        return { ...state, phrases: updatedPhrases };
      };
      return state;
    }
    case "DELETE_PHRASE": {
      const { index } = action;
      const updatedPhrases = [...state.phrases];
      const startIndex = updatedPhrases[index].startIndex;
      const stopIndex = updatedPhrases[index].stopIndex;
      updatedPhrases.splice(index, 1);

      const updatedSelectedIndices = state.selectedIndices.filter(
        i => i < startIndex || stopIndex < i
      );

      if (state.blockRefs) {
        const updatedBlockRefs = [...state.blockRefs];
        for (let i = startIndex; i <= stopIndex; i++) {
          const ref = updatedBlockRefs[i];
          if (ref && ref.current) {
            ref.current.classList.remove("text-block-0");
            ref.current.classList.remove("bg-light");
          }
        };
        return {
          ...state,
          phrases: updatedPhrases,
          selectedIndices: updatedSelectedIndices,
          blockRefs: updatedBlockRefs
        };
      };
      return {
        ...state,
        phrases: updatedPhrases,
        selectedIndices: updatedSelectedIndices
      };
    }
    default:
      return state;
  }
};


export default reducer;
