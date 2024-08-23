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
              const spaceRef = prevBlockRefs[index - 1];
              if (spaceRef !== null) {
                const spanElement = spaceRef.current;
                if (spanElement) {
                  spanElement.classList.add("text-block-0");
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
              const spaceRef = prevBlockRefs[index + 1];
              if (spaceRef !== null) {
                const spanElement = spaceRef.current;
                if (spanElement) {
                  spanElement.classList.add("text-block-0");
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

    const blocks = paragraphSplit.filter((p) => p.trim() !== "").flatMap((p, i) => {
      const words = p.split(" ").flatMap((word, j) => {
        const refWord = createRef<HTMLSpanElement>();
        const refSpace = createRef<HTMLSpanElement>();
        refs.push(...[refWord, refSpace]);

        return [
          // Word span
          <span
            className={"text-block font-l"}
            onClick={(e) => handleBlockClick(j * 2, e.target as HTMLSpanElement)}
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
          )
        ]
      });

      refs.push(null);  // don't include a ref for the <br /> element
      return [...words, <br key={i} />]
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
          <div className="grow column mb1">
            {showInput ? <TextField
              className={"font-l"}
              type={"textarea"}
              placeholder={"Paste your content here..."}
              onKeyup={setInputText}
              value={dummyText}
            /> : blocks}
          </div>
          <div className="justify-center">
            <AsyncButton
              onClick={handleInput}
              children={<span className="font-l">Start learning</span>}
              type="primary"
              size="xlarge"
            />
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
