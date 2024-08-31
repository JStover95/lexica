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


const Dashboard: React.FC = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { showInput, blocks, blockRefs, phrases } = state;

  // Effect to update block refs
  useEffect(() => {
    if (blockRefs) {
      blockRefs.forEach((ref, i) => {
        if (ref && ref.current && ref.current.innerHTML !== "&nbsp;") {
          ref.current.onclick = () =>
            dispatch({ type: "CLICK_BLOCK", index: i });
        }
      });
    }
  }, [blockRefs, dispatch]);

  useEffect(() => {
    phrases.forEach(async (phrase, i) => {
      if (phrase.active) {
        const element = phraseCardRefs[i].current;
        const container = element?.parentElement;
        if (element && container) scrollToTop(container, element);
        phrase.refs.forEach(ref => ref.current?.classList.add("bg-light"));
      } else {
        phrase.refs.forEach(ref => ref.current?.classList.remove("bg-light"));
      };

      phrase.refs.forEach(ref => {
        if (ref.current && ref.current.innerHTML != "&nbsp;") {
          ref.current.onclick = () => handleClickActiveBlock(i);
        };
      });

      if (phrase.dictionaryEntries) {
        return;
      };

      const query = phrase.refs.reduce((prev, current) => {
        if (current.current && current.current.innerHTML != "&nbsp;") {
          return `${prev} ${current.current.innerHTML}`;
        }
        return prev;
      }, "").trim();

      let context = "";
      let index = phrase.startIndex;
      if (blockRefs) {
        if (
          index > 0
          && blockRefs[index]?.current?.innerHTML.endsWith(".")
          && !blockRefs[index - 1]?.current?.innerHTML.endsWith(".")
        ) {
          index--;
        }
        while (index > -1
          && blockRefs[index] !== null
          && !blockRefs[index]?.current?.innerHTML.endsWith(".")
        ) {
          index--;
        }
        index++;
        while (index < blockRefs.length && blockRefs[index] !== null) {
          if (blockRefs[index]?.current?.innerHTML != "&nbsp;") {
            context = `${context} ${blockRefs[index]?.current?.innerHTML}`;
          }
          if (blockRefs[index]?.current?.innerHTML.endsWith(".")) {
            break;
          }
          index++;
        }
      }

      const inference = await fetch(process.env.REACT_APP_API_ENDPOINT + "/infer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"Query": query, "Context": context.trim()})
      });

      const result = await inference.json();
      const entries: IDictionaryEntry[] = result.Result;
      dispatch({ type: "GET_DICTIONARY_ENTRIES", index: i, entries: entries });
    });
  }, [phrases, dispatch])

  const handleClickStart = async () => {
    dispatch({ type: "CLICK_START" });
  };

  const handleClickPhraseCard = (index: number) => {
    dispatch({ type: "CLICK_PHRASE_CARD", index });
  };

  const handleClickActiveBlock = (index: number) => {
    const element = phraseCardRefs[index].current;
    const container = element?.parentElement;
    if (element && container) scrollToMiddle(container, element);
    dispatch({ type: "CLICK_PHRASE", index });
  };

  const handleClickDefinitionButton = (phraseIx: number, entryIx: number) => {
    dispatch({ type: "CLICK_SEE_MORE_DEFINITIONS", phraseIx, entryIx });
  };

  const handleClickStarButton = (phraseIx: number, entryIx: number, senseIx: number) => {
    dispatch({ type: "CLICK_STAR_BUTTON", phraseIx, entryIx, senseIx })
  };

  const phraseCardRefs: RefObject<HTMLDivElement>[] = [];
  const phraseCards = phrases.map((phrase, i) => {
    const ref = createRef<HTMLDivElement>();
    phraseCardRefs.push(ref);
    return (
      <div className="mb1" key={i} ref={ref}>
        <div
          className="font-l p1 border-mid border-radius hover-pointer hover-bg-light"
          onClick={() => handleClickPhraseCard(i)}
        >
          {phrase.refs.reduce((prev, current) => {
            if (current.current && current.current.innerHTML != "&nbsp;") {
              return `${prev} ${current.current.innerHTML}`;
            }
            return prev
          }, "")}
        </div>
        {phrase.active && phrase.dictionaryEntries && (
          <div className="mt1 ph1">
            {phrase.dictionaryEntries.map((entry, j) => {

              // get index of sense with highest rank
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
                  <span className="font-l mr1"><b>{entry.writtenForm}</b></span>
                  <span>{entry.partOfSpeech}</span>
                  <ol>
                    {entry.senses.map((sense, k) => {
                      const eq = sense.equivalents?.find(
                        eq => eq.equivalentLanguage == "영어"
                      );

                      return (
                        <li key={`${i}-${j}-${k}`} className={(entry.showAll || maxIndex === k) ? "mb0-5" : "hidden" }>
                          <div className="grow">
                            <div className="column">
                              {eq && <span>{eq.equivalent}</span>}
                              <span>{sense.definition}</span>
                              {eq && <span>{eq.definition}</span>}
                              {!entry.showAll && entry.senses.length > 1 && <span
                                className="border-radius btn btn-primary font-s mt0-5 w-fit-content"
                                onClick={() => handleClickDefinitionButton(i, j)}
                              >
                                See more definitions
                              </span>}
                            </div>
                            {entry.senses.length > 1 && (maxIndex === k
                              ? (
                                <div className="flex-grow align-center justify-end grow hover-pointer">
                                  <i className="material-icons icon-primary-mid icon-l p1"
                                    onClick={() => entry.showAll && handleClickStarButton(i, j, k)}
                                  >
                                    star
                                  </i>
                                </div>
                              )
                              : (
                                <div className="flex-grow align-center justify-end grow icon-hover">
                                  <i className="material-icons icon-l hover-pointer p1"
                                    onClick={() => entry.showAll && handleClickStarButton(i, j, k)}
                                  >
                                    star
                                  </i>
                                </div>
                            ))}
                          </div>
                        </li>
                      );
                    })}
                  </ol>
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  });

  return (
    <div className="column grow align-center">
      <div>
        <h1>MyMaum</h1>
      </div>
      <div className="flex w100p">
        <div className="grow column p2 w50p h800">
          {showInput ? 
            <div className="grow column mb1">
              <TextField
                className={"font-l"}
                type={"textarea"}
                placeholder={"Paste your content here..."}
                onKeyup={(text) => dispatch({ type: "EDIT_INPUT", text })}
                value={dummyText}
              />
            </div> :
            <div className="font-height-l scroll pr1">
              {blocks}
            </div>
          }
          <div className="justify-center">
            {showInput && <AsyncButton
              onClick={handleClickStart}
              children={<span className="font-l">Start learning</span>}
              type="primary"
              size="xlarge"
            />}
          </div>
        </div>
        <div className="grow column p2 w50p h800">
          <div className="scroll pr1">
            {phraseCards}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
