import { createRef, RefObject } from "react";
import { IDashboardState } from "../interfaces";


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

      if (!state.selectedIndices.includes(index)) {
        const updatedSelectedIndices = [...state.selectedIndices, index];
        const block = state.blockRefs?.[index]?.current;
        block?.classList.add("text-block-0");

        // Check for adjacent words
        if (state.selectedIndices.includes(index - 2)) {
          updatedSelectedIndices.push(index - 1);
          if (state.blockRefs) {
            const spanRef = state.blockRefs[index - 2];
            if (spanRef?.current && !spanRef.current.innerHTML.endsWith(".")) {
              const spaceElement = state.blockRefs[index - 1]?.current;
              spaceElement?.classList.add("text-block-0");
            }
          }
        }

        if (state.selectedIndices.includes(index + 2)) {
          updatedSelectedIndices.push(index + 1);
          if (state.blockRefs) {
            const spanRef = state.blockRefs[index];
            if (spanRef?.current && !spanRef.current.innerHTML.endsWith(".")) {
              const spaceElement = state.blockRefs[index + 1]?.current;
              spaceElement?.classList.add("text-block-0");
            }
          }
        }

        return { ...state, selectedIndices: updatedSelectedIndices };
      }
      return state;
    }
    default:
      return state;
  }
};


export default reducer;
