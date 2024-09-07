import { createRef, RefObject } from "react";
import { IDashboardState, IDictionaryEntry, IPhrase } from "../utils/interfaces";
import { scrollToMiddle } from "../utils/utils";

type Action =
  | { type: "EDIT_INPUT"; text: string }
  | { type: "CLICK_START" }
  | { type: "CLICK_BLOCK"; index: number }
  | { type: "CLICK_PHRASE_CARD"; index: number }
  | { type: "CLICK_ACTIVE_BLOCK"; index: number }
  | { type: "CLICK_SEE_MORE_DEFINITIONS"; phraseIx: number; entryIx: number }
  | { type: "CLICK_SENSE_BUTTON"; phraseIx: number; entryIx: number; senseIx: number; }
  | { type: "GET_DICTIONARY_ENTRIES"; previousText: string; index: number; entries: IDictionaryEntry[] }
  | { type: "DELETE_PHRASE"; index: number };


/**
 * Reducer function to manage the state of a dashboard.
 * 
 * The dashboard displays text broken down into blocks, where each block can
 * represent a word, space, or paragraph break. The application allows various
 * user interactions such as editing text input, clicking on blocks, phrases,
 * and fetching dictionary entries. This reducer handles these actions and
 * updates the state accordingly.
 * 
 * @param {IDashboardState} state - The current dashboard state.
 * @param {Action} action - The dispatched action describing the change.
 * @returns {IDashboardState} - The updated state after applying the action.
 */
const reducer = (state: IDashboardState, action: Action) => {
  switch (action.type) {
    case "EDIT_INPUT": {

      // Update the dashboard's input text
      const { text } = action;
      return { ...state, inputText: text };
    }
    case "CLICK_START": {

      // If there is no input text, do nothing
      if (state.inputText === "") return state;

      // Split text by paragraphs
      const paragraphSplit = state.inputText.split(/\n+/);

      // Create a list of refs to each block that will be created in this function
      const blockRefs: (RefObject<HTMLSpanElement> | null)[] = [];

      // Create a list of blocks
      const blocks = paragraphSplit
        .filter((p) => p.trim() !== "")  // Skip empty paragraphs
        .flatMap((p, i) => {

          // Split the paragraph into words and iterate over every word
          const words = p.split(" ").flatMap((word, j) => {

            // Whether the current word is at the end of the paragraph
            const isEndOfParagraph = !(j < p.split(" ").length - 1);

            // Create a ref for the word block and the following white space block
            const refWord = createRef<HTMLSpanElement>();
            const refSpace = createRef<HTMLSpanElement>();

            // If the current word is the end of the paragraph
            if (isEndOfParagraph) {

              // Don't push the following white space block ref
              blockRefs.push(refWord);
            } else {
              blockRefs.push(refWord, refSpace);
            }

            const result = [
              // The word block
              <span
                className={"text-block font-l"}
                key={`word-${i}-${j}`}
                ref={refWord}
              >
                {word}
              </span>
            ];

            // If the current word is not the end of the paragraph, push the white space block
            if (!isEndOfParagraph) {
              result.push(
                // The space block 
                <span
                  className={"text-block font-l"}
                  key={`space-${i}-${j}`}
                  ref={refSpace}
                >
                  &nbsp;
                </span>
              );
            };

            return result;
          });

          // The end of each paragraph will always have two <br /> elements corresponding to null entries in blockRefs
          blockRefs.push(null, null);
          return [...words, <br key={`b1-${i}`} />, <br key={`b2-${i}`} />];
        });

      return { ...state, blocks, blockRefs, showInput: false };
    }
    case "CLICK_BLOCK": {
      const { index } = action;

      // If the user clicks a block that is not part of a phrase
      if (
        !state.selectedIndices.includes(index)
        && state.blockRefs?.[index]?.current
      ) {
        const blockRef = state.blockRefs[index];
        const block = state.blockRefs[index]?.current;

        if (block && blockRef) {
          const updatedSelectedIndices = [...state.selectedIndices, index];
          const updatedPhrases = [...state.phrases];

          // Make all phrases inactive
          updatedPhrases.forEach(phrase => phrase.active = false);

          // Underline the block
          block.classList.add("text-block-0");

          // Always create a new phrase on each click of a new block
          const newPhrase: IPhrase = {
            active: true,
            startIndex: index,
            stopIndex: index,
            refs: [blockRef],
            dictionaryEntries: null,
            explanation: "",
            previousText: "",
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
              newPhrase.startIndex = updatedPhrases[leftPhraseIx].startIndex;
              newPhrase.dictionaryEntries = updatedPhrases[leftPhraseIx]
                .dictionaryEntries;
              newPhrase.previousText = updatedPhrases[leftPhraseIx].previousText;
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

            // If the current block is not the end of a sentence
            if (!state.blockRefs[index]?.current?.innerHTML.endsWith(".")) {
              const spaceRef = state.blockRefs[index + 1];
              const spaceElement = spaceRef?.current;
              spaceElement?.classList.add("text-block-0");
              newPhrase.stopIndex = updatedPhrases[rightPhraseIx].stopIndex;
              newPhrase.dictionaryEntries = updatedPhrases[rightPhraseIx]
                .dictionaryEntries;
              newPhrase.previousText = updatedPhrases[rightPhraseIx].previousText;
              newPhrase.refs = [
                ...newPhrase.refs,
                ...(spaceRef ? [spaceRef] : []),
                ...updatedPhrases[rightPhraseIx].refs
              ];
              updatedPhrases.splice(rightPhraseIx, 1);
            }
          }

          // Add the new phrase
          updatedPhrases.push(newPhrase);

          // Sort phrases by start index
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

      // Get the phrase's first block in the text view and its parent container
      const container = updatedPhrases[index].refs[0].current?.parentElement;
      const element = updatedPhrases[index].refs[0].current;

      // Scroll the first block to the middle of the parent container
      if (container && element) scrollToMiddle(container, element);

      // Make the clicked phrase active
      updatedPhrases.forEach((phrase, i) => phrase.active = index == i);
      return { ...state, phrases: updatedPhrases };
    }
    case "CLICK_ACTIVE_BLOCK": {
      const { index } = action;
      const updatedPhrases = [...state.phrases];

      // Set the phrase that contains the active block to active
      updatedPhrases.forEach((phrase, i) => phrase.active = index == i);
      return { ...state, phrases: updatedPhrases };
    }
    case "CLICK_SEE_MORE_DEFINITIONS": {
      const { phraseIx, entryIx } = action;

      // Get the phrase that contains the definition that was clicked
      const updatedPhrases = [...state.phrases];
      const phrase = updatedPhrases[phraseIx];

      // Show all of the definition's senses
      if (phrase.dictionaryEntries) {
        const entry = phrase.dictionaryEntries[entryIx].showAll = true;
      }
      return { ...state, phrases: updatedPhrases };
    }
    case "CLICK_SENSE_BUTTON": {
      const { phraseIx, entryIx, senseIx } = action;

      // Get the phrase and dictionary entry that contain the sense that was clicked
      const updatedPhrases = [...state.phrases];
      const phrase = updatedPhrases[phraseIx];
      if (phrase.dictionaryEntries) {
        const entry = phrase.dictionaryEntries[entryIx];
        entry.showAll = false;

        // The sense with the highest rank is always shown, so set the rank of this to 1 and all others to 0
        entry.senses.forEach(sense => {
          if (sense.rank === 1.0) sense.rank = 0.0;
        });
        entry.senses[senseIx].rank = 1.0;
      }
      return { ...state, phrases: updatedPhrases };
    }
    case "GET_DICTIONARY_ENTRIES": {
      const { previousText, index, entries } = action;

      // Get the phrase corresponding to the dictionary entris
      const updatedPhrases = [...state.phrases];
      const phrase = updatedPhrases[index];

      // Set the phrase's dictionary entries
      if (phrase && phrase.previousText !== previousText) {

        // If the phrase already has dictionary entries
        if (updatedPhrases[index].dictionaryEntries) {
          updatedPhrases[index].dictionaryEntries?.push(...entries);
        } else {
          updatedPhrases[index].dictionaryEntries = entries;
        }

        // Keep track of the phrase's previous text
        updatedPhrases[index].previousText = previousText;
        return { ...state, phrases: updatedPhrases };
      };
      return state;
    }
    case "DELETE_PHRASE": {
      const { index } = action;
      const updatedPhrases = [...state.phrases];
      const startIndex = updatedPhrases[index].startIndex;
      const stopIndex = updatedPhrases[index].stopIndex;

      // Remove the phrase from the state
      updatedPhrases.splice(index, 1);

      // Remove the phrase's blocks from selected indices
      const updatedSelectedIndices = state.selectedIndices.filter(
        i => i < startIndex || stopIndex < i
      );

      if (state.blockRefs) {

        // Iterate over the phrase's blocks
        const updatedBlockRefs = [...state.blockRefs];
        for (let i = startIndex; i <= stopIndex; i++) {
          const ref = updatedBlockRefs[i];

          // Remove any underline and highlight
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
