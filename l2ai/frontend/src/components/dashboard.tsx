import React, { createRef, RefObject, useEffect, useState } from "react";

import "../styleSheets/styles.css";
import TextField from "./fields/textField";
import AsyncButton from "./buttons/asyncButton";

import { dummyText } from "../dummyData";


const Dashboard: React.FC = () => {
  const [inputText, setInputText] = useState<string>(dummyText);
  const [showInput, setShowInput] = useState<Boolean>(true);
  const [blocks, setBlocks] = useState<React.ReactNode[] | null>(null);
  const [blockRefs, setBlockRefs] = useState<(RefObject<HTMLSpanElement> | null)[] | null>(null);
  const [selectedIndices, setSelectedIndices] = useState<number[]>([]);

  const handleBlockClick = (index: number, block: HTMLSpanElement) => {
    setSelectedIndices((prevSelectedIndices) => {

      // Check if the word is already selected
      if (!prevSelectedIndices.includes(index)) {

        // Create a new array with the updated selected indices
        const updatedSelectedIndices = [...prevSelectedIndices, index];
        block.classList.add("text-block-0");  // Set the word as active
  
        // Check for adjacent words
        if (prevSelectedIndices.includes(index - 2)) {

          // If the previous word is selected, select the space in between
          updatedSelectedIndices.push(index - 1);
          setBlockRefs((prevBlockRefs) => {
            if (prevBlockRefs !== null) {

              // skip if the adjacent word is the end of a sentence
              const spanRef = prevBlockRefs[index - 2];
              if (spanRef !== null) {
                const spanElement = spanRef.current;
                if (spanElement !== null && spanElement.innerHTML.endsWith(".")) {
                  return prevBlockRefs;
                }
              }

              const spaceRef = prevBlockRefs[index - 1];
              if (spaceRef !== null) {
                const spaceElement = spaceRef.current;
                if (spaceElement) {
                  spaceElement.classList.add("text-block-0");
                }
              }
            }
            return prevBlockRefs;
          });
        }
        
        if (prevSelectedIndices.includes(index + 2)) {

          // If the next word is selected, select the space in between
          updatedSelectedIndices.push(index + 1);
          setBlockRefs((prevBlockRefs) => {
            if (prevBlockRefs !== null) {

              // skip if the current word is the end of a sentence
              const spanRef = prevBlockRefs[index];
              if (spanRef !== null) {
                const spanElement = spanRef.current;
                if (spanElement !== null && spanElement.innerHTML.endsWith(".")) {
                  return prevBlockRefs;
                }
              }

              const spaceRef = prevBlockRefs[index + 1];
              if (spaceRef !== null) {
                const spaceElement = spaceRef.current;
                if (spaceElement) {
                  spaceElement.classList.add("text-block-0");
                }
              }
            }
            return prevBlockRefs;
          });
        }
  
        return updatedSelectedIndices;
      }
  
      // If the word was already selected, return the previous state unchanged
      return prevSelectedIndices;
    });
  };

  const handleInput = async () => {
    if (inputText === "") return;
    const paragraphSplit = inputText.split(/\n+/);  // Splits text by paragraphs
    const refs: (RefObject<HTMLSpanElement> | null)[] = [];
    let counter = -1;
  
    const blocks = paragraphSplit
      .filter((p) => p.trim() !== "")
      .flatMap((p, i) => {
        const words = p.split(" ").flatMap((word, j) => {
          const refWord = createRef<HTMLSpanElement>();
          const refSpace = createRef<HTMLSpanElement>();
  
          // Capture the current value of counter
          const currentCounter = counter + 1;
          refs.push(...[refWord, refSpace]);
          counter = currentCounter;  // Update the counter after capturing it
  
          return [
            // Word span
            <span
              className={"text-block font-l"}
              onClick={(e) =>
                handleBlockClick(currentCounter * 2, e.target as HTMLSpanElement)
              }
              key={`word-${i}-${j}`}
              ref={refWord}
            >
              {word}
            </span>,
  
            // Space span
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
  
        counter += 1; // Increment counter for the next iteration
        refs.push(...[null, null]);  // Don't include refs for the <br /> elements
        return [...words, <br key={`b1-${i}`} />, <br key={`b2-${i}`} />];
      });
  
    setBlocks(blocks);
    setBlockRefs(refs);
    setShowInput(false);
  };
  

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
                onKeyup={setInputText}
                value={dummyText}
              />
            </div> :
            <div className="font-height-l scroll pr1">
              {blocks}
            </div>
          }
          <div className="justify-center">
            {showInput && <AsyncButton
              onClick={handleInput}
              children={<span className="font-l">Start learning</span>}
              type="primary"
              size="xlarge"
            />}
          </div>
        </div>
        <div className="grow p2 w50p h800">
          <span>Feedback area</span>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
