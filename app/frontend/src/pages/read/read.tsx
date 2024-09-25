import React, { RefObject, useEffect, useReducer } from "react";
import { dummyText } from "../../utils/dummyData";
import { IDictionaryEntry, IReadState } from "../../utils/interfaces";
import reducer from "./readReducer";
import { scrollToTop } from "../../utils/utils";
import ViewPhrasesButton from "../../components/buttons/viewPhrasesButton";

export const initialState: IReadState = {
  blocks: null,
  blockRefs: null,
  selectedIndices: [],
  phrases: [],
};


const Read: React.FC = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { blocks, blockRefs, phrases } = state;

  // Initialize blocks
  useEffect(() => {
    dispatch({ type: "INIT_BLOCKS", text: dummyText });
  }, []);

  // References to store the phrase card elements
  const phraseCardRefs: RefObject<HTMLDivElement>[] = [];

  /**
   * Updates block refs and attaches click handlers to refs when blockRefs
   * changes.
   */
  useEffect(() => {
    if (blockRefs) {
      blockRefs.forEach((ref, i) => {

        // // If the ref's element is not whitespace between two words
        // if (ref && ref.current && ref.current.innerHTML !== "&nbsp;") {
        //   ref.current.onclick = () => dispatch(
        //     { type: "CLICK_BLOCK", index: i }
        //   );
        // }
      });
    }
  }, [blockRefs, dispatch]);

  /**
   * Updates phrase highlights and attaches click handlers to phrases when
   * phrases changes. Also fetches dictionary entries for active phrases.
   */
  useEffect(() => {
    phrases.forEach(async (phrase, i) => {

      // If the phrase is being viewed by the user
      if (phrase.active) {

        // Get the phrase card's element
        const element = phraseCardRefs[i].current;

        // Get the phrase card's parent and scroll the parent so that the phrase card is at the top of the container
        const container = element?.parentElement;
        if (element && container) scrollToTop(container, element);

        // Highlight the phrase in the text view
        phrase.refs.forEach(ref => ref.current?.classList.add("bg-light"));
      }
      
      // If the phrase is not being viewed by the user
      else {

        // Remove any highlight from the phrase in the text view
        phrase.refs.forEach(ref => ref.current?.classList.remove("bg-light"));
      };

      // Add an on click event to the phrase in the text view
      phrase.refs.forEach(ref => {
        if (ref.current && ref.current.innerHTML != "&nbsp;") {
          ref.current.onclick = () => handleClickActiveBlock(i);
        };
      });

      // Combine the phrase's refs into a single space-separated string of unique words
      let phraseText = "";
      phrase.refs.forEach(ref => {
        if (
          ref.current
          && ref.current.innerHTML != "&nbsp;"
          && !phraseText.includes(ref.current.innerHTML)
        ) {
          phraseText = `${phraseText} ${ref.current.innerHTML}`;
        }
      });

      // If the phrase does not have any new words to query, skip querying the dictionary
      if (phrase.previousText === phraseText) {
        return;
      };

      // Query only the newly selected words
      const query = phraseText.replace(phrase.previousText, "").trim();

      // Get the whole sentence that the phrase is part of to pass as context
      let context = "";
      let index = phrase.startIndex;
      if (blockRefs) {

        // If the start of the phrase is the end of the sentence, navigate left by one index
        if (
          index > 0
          && blockRefs[index]?.current?.innerHTML.endsWith(".")
          && !blockRefs[index - 1]?.current?.innerHTML.endsWith(".")
        ) {
          index--;
        };

        // Navigate left until passing the beginning or reaching a line break or the end of the previous sentence
        while (
          index > -1
          && blockRefs[index] !== null
          && !blockRefs[index]?.current?.innerHTML.endsWith(".")
        ) {
          index--;
        }

        // Navigate right one to set the pointer to the first word of the sentence
        index++;

        // Navigate right and build the string until reaching the end of the text or a line break
        while (index < blockRefs.length && blockRefs[index] !== null) {
          if (blockRefs[index]?.current?.innerHTML != "&nbsp;") {
            context = `${context} ${blockRefs[index]?.current?.innerHTML}`;
          }

          // Brek when the word is the end of the sentence
          if (blockRefs[index]?.current?.innerHTML.endsWith(".")) {
            break;
          }
          index++;
        }
      }

      // Get the inference
      const inference = await fetch(
        process.env.REACT_APP_API_ENDPOINT + "/infer",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ "Query": query, "Context": context.trim() })
        }
      );

      const result = await inference.json();
      const entries: IDictionaryEntry[] = result.Result;

      // Set the dictionary entries
      dispatch({
        type: "SET_DICTIONARY_ENTRIES",
        previousText: phraseText,
        index: i,
        entries
      });
    });
  }, [phrases, dispatch]);

  /**
   * Handler for the phrase card click event.
   * 
   * @param index - The index of the clicked phrase card.
   */
  const handleClickPhraseCard = (index: number) => {
    dispatch({ type: "CLICK_PHRASE_CARD", index });
  };

  /**
   * Handler for an active block click event. This scrolls the phrase's card
   * to the top of the feedback view and sets it to active.
   * 
   * @param index - The index of the clicked active block.
   */
  const handleClickActiveBlock = (index: number) => {
    const element = phraseCardRefs[index].current;
    const container = element?.parentElement;
    if (element && container) scrollToTop(container, element);
    dispatch({ type: "CLICK_ACTIVE_BLOCK", index });
  };

  /**
   * Handler for the definition button click event.
   * 
   * @param phraseIx - The index of the phrase containing the definition.
   * @param entryIx - The index of the dictionary entry that was visible.
   */
  const handleClickDefinitionButton = (phraseIx: number, entryIx: number) => {
    dispatch({ type: "CLICK_SEE_MORE_DEFINITIONS", phraseIx, entryIx });
  };

  const handleClickViewPhrasesButton = () => {}

  return (
    <>
      <div className="flex-grow px-8 pt-8 w-full overflow-y-scroll overflow-x-hidden">
        {blocks}
      </div>
      <ViewPhrasesButton onClick={handleClickViewPhrasesButton} />
    </>
  );
};


export default Read
