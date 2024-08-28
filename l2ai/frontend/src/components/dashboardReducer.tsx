import { createRef, RefObject } from "react";
import { IDashboardState, IPhrase } from "../interfaces";


type Action =
  | { type: "EDIT_INPUT"; text: string }
  | { type: "CLICK_START" }
  | { type: "CLICK_BLOCK"; index: number };


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

      if (!state.selectedIndices.includes(index) && state.blockRefs?.[index]?.current) {
        const blockRef = state.blockRefs[index];
        const block = state.blockRefs[index]?.current;

        if (block && blockRef) {
          const updatedSelectedIndices = [...state.selectedIndices, index];
          const updatedPhrases = [...state.phrases];
          block.classList.add("text-block-0");

          const newPhrase: IPhrase = { startIndex: index, stopIndex: index, refs: [blockRef], explanation: "" };

          // Check for adjacent words
          if (state.selectedIndices.includes(index - 2)) {
            const leftPhraseIx = updatedPhrases.findIndex(phrase => phrase.stopIndex == index - 2);
            if (!(block.innerHTML.endsWith(".") || updatedPhrases[leftPhraseIx].explanation !== "")) {
              newPhrase.startIndex = updatedPhrases[leftPhraseIx].startIndex;
              newPhrase.refs = [...updatedPhrases[leftPhraseIx].refs, ...newPhrase.refs];
              updatedPhrases.splice(leftPhraseIx, 1);
              const spaceElement = state.blockRefs[index - 1]?.current;
              spaceElement?.classList.add("text-block-0");
            }
          }

          if (state.selectedIndices.includes(index + 2)) {
            const rightPhraseIx = updatedPhrases.findIndex(phrase => phrase.startIndex == index + 2);
            if (!(block.innerHTML.endsWith(".") || updatedPhrases[rightPhraseIx].explanation !== "")) {
              newPhrase.stopIndex = updatedPhrases[rightPhraseIx].startIndex;
              newPhrase.refs = [...newPhrase.refs, ...updatedPhrases[rightPhraseIx].refs];
              updatedPhrases.splice(rightPhraseIx, 1);
              const spaceElement = state.blockRefs[index + 1]?.current;
              spaceElement?.classList.add("text-block-0");
            }
          }

          updatedPhrases.push(newPhrase);
          return { ...state, selectedIndices: updatedSelectedIndices, phrases: updatedPhrases };
        }
      }
      return state;
    }
    default:
      return state;
  }
};


export default reducer;
