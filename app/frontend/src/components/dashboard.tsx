import React, { createRef, RefObject, useEffect, useReducer } from "react";

import { IDashboardState, IDictionaryEntry } from "../interfaces";
import "../styleSheets/styles.css";
import TextField from "./fields/textField";
import AsyncButton from "./buttons/asyncButton";
import reducer from "./dashboardReducer";

import { dummyText } from "../dummyData";
import { scrollToMiddle, scrollToTop } from "../utils";

const initialState: IDashboardState = {
  inputText: dummyText,
  showInput: true,
  blocks: null,
  blockRefs: null,
  selectedIndices: [],
  phrases: [],
};

/**
 * Dashboard functional component for displaying and interacting with phrases.
 * Uses useReducer for state management and useEffect for side effects.
 */
const Dashboard: React.FC = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { showInput, blocks, blockRefs, phrases } = state;

  /**
   * Updates block refs and attaches click handlers to refs when blockRefs
   * changes.
   */
  useEffect(() => {
    if (blockRefs) {
      blockRefs.forEach((ref, i) => {

        // If the ref's element is not whitespace between two words
        if (ref && ref.current && ref.current.innerHTML !== "&nbsp;") {
          ref.current.onclick = () => dispatch(
            { type: "CLICK_BLOCK", index: i }
          );
        }
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

      // If the phrase already has dictionary entries, skip the rest of the function
      if (phrase.dictionaryEntries) {
        return;
      };

      // Combine the phrase's refs into a single space-separated string
      const query = phrase.refs.reduce((prev, current) => {
        if (current.current && current.current.innerHTML != "&nbsp;") {
          return `${prev} ${current.current.innerHTML}`;
        }
        return prev;
      }, "").trim();

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
      dispatch({ type: "GET_DICTIONARY_ENTRIES", index: i, entries: entries });
    });
  }, [phrases, dispatch]);

  /**
   * Handler for the start button click event.
   */
  const handleClickStart = async () => {
    dispatch({ type: "CLICK_START" });
  };

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

  /**
   * Handler for the sense button click event.
   * 
   * @param phraseIx - The index of the phrase containing the sense.
   * @param entryIx - The index of the dictionary entry.
   * @param senseIx - The index of the sense within the dictionary entry.
   */
  const handleClickSenseButton = (
    phraseIx: number, entryIx: number, senseIx: number
  ) => {
    dispatch({ type: "CLICK_SENSE_BUTTON", phraseIx, entryIx, senseIx });
  };

  // References to store the phrase card elements
  const phraseCardRefs: RefObject<HTMLDivElement>[] = [];
  
  // Render the phrase cards based on the state phrases
  const phraseCards = phrases.map((phrase, i) => {
    const ref = createRef<HTMLDivElement>();
    phraseCardRefs.push(ref);
    return (
      <div className="mb1" key={i} ref={ref}>

        {/* The phrase card header */}
        <div
          className="font-l p1 border-mid border-radius hover-pointer hover-bg-light align-center justify-space-between"
          onClick={() => handleClickPhraseCard(i)}
        >
          <span>
            {phrase.refs.reduce((prev, current) => {
              if (current.current && current.current.innerHTML != "&nbsp;") {
                return `${prev} ${current.current.innerHTML}`;
              }
              return prev;
            }, "")}
          </span>

          {/* The delete phrase button */}
          <span
            className="ph1 hover-icon-red justify-center"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              dispatch({ type: "DELETE_PHRASE", index: i });
            }}
          >
            <i className="material-icons">close</i>
          </span>
        </div>

        {/* The phrase's dictionary entries */}
        {phrase.active && phrase.dictionaryEntries &&
          <div className="mt1 ph1">
            {phrase.dictionaryEntries.map((entry, j) => {

              // Get the index of the sense with the highest rank
              let maxRank = 0;
              let maxIndex = 0;
              for (let index = 0; index < entry.senses.length; index++) {
                const rank = entry.senses[index].rank;
                if (rank && rank > maxRank) {
                  maxRank = rank;
                  maxIndex = index;
                }
              };

              return (
                <div key={`${i}-${j}`}>

                  {/* The sense's header including written form and part of speech */}
                  <span className="font-l mr1"><b>{entry.writtenForm}</b></span>
                  <span>{entry.partOfSpeech}</span>
                  <ol>

                    {/* The list of senses for this entry */}
                    {entry.senses.map((sense, k) => {
                      const eq = sense.equivalents?.find(
                        eq => eq.equivalentLanguage == "영어"
                      );

                      return (
                        <li
                          key={`${i}-${j}-${k}`}
                          className={
                            (entry.showAll || maxIndex === k)  // Either show all or only the sense with highest rank
                            ? "mb0-5"
                            : "hidden"
                          }
                        >
                          <div className="grow">

                            {/* The sense's definition */}
                            <div className="column">
                              {eq && <span>{eq.equivalent}</span>}
                              <span>{sense.definition}</span>
                              {eq && <span>{eq.definition}</span>}
                            </div>
                            {entry.senses.length > 1 && (maxIndex === k

                              // If this entry has multiple senses and this sense has the highest rank
                              ? (

                                // Show a checked radio button
                                <div className="flex-grow align-center justify-end grow hover-pointer">
                                  <i className="material-icons icon-primary-mid icon-l p1"
                                    onClick={
                                      () => {
                                        entry.showAll
                                        && handleClickSenseButton(i, j, k);
                                      }
                                    }
                                  >
                                    radio_button_checked
                                  </i>
                                </div>
                              )

                              // If this entry has multiple senses and this sense does not have the highest rank
                              : (

                                // Show an unchecked checkbox
                                <div className="flex-grow align-center justify-end grow icon-hover">
                                  <i className="material-icons icon-l hover-pointer p1"
                                    onClick={() => entry.showAll && handleClickSenseButton(i, j, k)}
                                  >
                                    radio_button_unchecked
                                  </i>
                                </div>
                              ))}
                          </div>

                          {/* If the entry has multiple senses and only one is shown */}
                          {!entry.showAll && entry.senses.length > 1 &&

                            // Show a button to choose a different definition
                            <span
                              className="font-s hover-pointer"
                              onClick={() => handleClickDefinitionButton(i, j)}
                            >
                              <u>Choose a different definition...</u>
                            </span>
                          }
                        </li>
                      );
                    })}
                  </ol>
                </div>
              );
            })}
          </div>
        }
      </div>
    );
  });

  return (
    <div className="column grow align-center">

      {/* Header */}
      <div>
        <h1>Lexica</h1>
      </div>
      <div className="flex w100p">

        {/* The text view */}
        <div className="grow column p2 w50p h800">
          {showInput ?

            // The input field
            <div className="grow column mb1">
              <TextField
                className={"font-l"}
                type={"textarea"}
                placeholder={"Paste your content here..."}
                onKeyup={(text) => dispatch({ type: "EDIT_INPUT", text })}
                prefill={dummyText}
              />
            </div> :

            // Processed input text for reading
            <div className="font-height-l scroll pr1">
              {blocks}
            </div>
          }

          {/* The "Start learning" button */}
          <div className="justify-center">
            {showInput && <AsyncButton
              onClick={handleClickStart}
              children={<span className="font-l">Start learning</span>}
              type="primary"
              size="xlarge"
            />}
          </div>
        </div>

        {/* The feedback view */}
        <div className="grow column p2 w50p h800">
          <div className="scroll pr1">
            {phraseCards}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard;
