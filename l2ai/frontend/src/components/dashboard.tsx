import React, { useEffect, useReducer } from "react";

import { IDashboardState } from "../interfaces";
import "../styleSheets/styles.css";
import TextField from "./fields/textField";
import AsyncButton from "./buttons/asyncButton";
import reducer from "./dashboardReducer";

import { dummyDefinition, dummyText } from "../dummyData";

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
          ref.current.onclick = (e) =>
            dispatch({ type: "CLICK_BLOCK", index: i });
        }
      });
    }
  }, [blockRefs, dispatch]);

  useEffect(() => {
    phrases.forEach((phrase, i) => {
      if (!phrase.dictionaryEntries) {
        // TODO: make request
        dispatch({ type: "GET_DICTIONARY_ENTRIES", index: i, entries: phrase.refs.map(() => dummyDefinition) });
      }
    });
  }, [phrases, dispatch])

  const handleClickStart = async () => {
    dispatch({ type: "CLICK_START" });
  };

  const phraseCards = phrases.map((phrase, i) => {
    return (
      <div className="mb1" key={i}>
        <div className="font-l p1 border-mid border-radius">
          {phrase.refs.reduce((prev, current) => {
            if (current.current) {
              return `${prev} ${current.current.innerHTML}`;
            }
            return prev
          }, "")}
        </div>
        {phrase.dictionaryEntries && (
          <div className="mt1 ph1">
            {phrase.dictionaryEntries.map((entry, j) => (
              <div key={`${i}-${j}`}>
                <span className="font-l mr1"><b>{entry.writtenForm}</b></span>
                <span>{entry.partOfSpeech}</span>
                <ol>
                  {entry.senses.map((sense, k) => {
                    const eq = sense.equivalents.find(
                      eq => eq.equivalentLanguage == "영어"
                    );

                    return (
                      <li key={`${i}-${j}-${k}`} className="mb0-5">
                        <div className="column">
                          {eq && <span>{eq.equivalent}</span>}
                          <span>{sense.definition}</span>
                          {eq && <span>{eq.definition}</span>}
                        </div>
                      </li>
                    );
                  })}
                </ol>
              </div>
            ))}
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
          {phraseCards}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
