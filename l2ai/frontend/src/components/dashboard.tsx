import React, { createRef, RefObject, useEffect, useReducer } from "react";

import { IDashboardState, IDictionaryEntry } from "../interfaces";
import "../styleSheets/styles.css";
import TextField from "./fields/textField";
import AsyncButton from "./buttons/asyncButton";
import reducer from "./dashboardReducer";

import { dummyDefinition, dummyText } from "../dummyData";
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
      phrase.refs.forEach(ref => {
        if (ref.current) {
          ref.current.onclick = () => handleClickActiveBlock(i);
        };
      });

      if (phrase.dictionaryEntries) {
        return;
      };

      const query = phrase.refs.reduce((prev, current) => {
        if (current.current) {
          return `${prev} ${current.current.innerHTML}`;
        }
        return prev;
      }, "").trim();

      let context = "";
      if (blockRefs) {
        if  (blockRefs[phrase.startIndex - 2] !== null) {
          const text = blockRefs[phrase.startIndex - 2]?.current?.innerHTML;
          if (text) context = text;
        }
        context = `${context} ${query}`.trim();
        if  (blockRefs[phrase.stopIndex + 2] !== null) {
          context = `${context} ${blockRefs[phrase.stopIndex + 2]?.current?.innerHTML}`.trim();
        }
      }

      const graphqlQuery = {
        query: `
          query SearchDictionary($q: String!, $lang: String!, $context: String!) {
            searchDictionary(q: $q, lang: $lang, context: $context) {
              writtenForm
              partOfSpeech
              senses {
                definition
                equivalents {
                  equivalentLanguage
                  equivalent
                  definition
                }
              }
            }
          }
        `,
        variables: {
          q: query,
          lang: "영어",  // TODO: allow user to select
          context: context,
        },
      };

      try {
        const response = await fetch(process.env.REACT_APP_API_ENDPOINT + "/graphql", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(graphqlQuery),
        });

        const result = await response.json();
        const entries: IDictionaryEntry[] = result.data.searchDictionary;
        dispatch({ type: "GET_DICTIONARY_ENTRIES", index: i, entries: entries });
      } catch (error) {
        console.error("Error fetching dictionary entry:", error);
      }
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
    if (element && container) scrollToTop(container, element);
    dispatch({ type: "CLICK_PHRASE", index });
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
            if (current.current) {
              return `${prev} ${current.current.innerHTML}`;
            }
            return prev
          }, "")}
        </div>
        {phrase.active && phrase.dictionaryEntries && (
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
          <div className="scroll pr1">
            {phraseCards}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
