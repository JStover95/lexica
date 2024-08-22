import React, { useState } from "react";

import "../styleSheets/styles.css";
import TextField from "./fields/textField";
import AsyncButton from "./buttons/asyncButton";

import { dummyText } from "../dummyData";


const Dashboard: React.FC = () => {
  const [inputText, setInputText] = useState<string>(dummyText);
  const [showInput, setShowInput] = useState<Boolean>(true);
  const [outputBlocks, setOutputBlocks] = useState<React.ReactNode | null>(null);
  const [activeBlocks, setActiveBlocks] = useState<number[]>([]);

  const handleBlockClick = (i: number, block: HTMLSpanElement) => {
    if (!activeBlocks.includes(i)) {
      activeBlocks.push(i);
      setActiveBlocks(activeBlocks);
      block.classList.add("text-block-active");
    };
  };

  const handleInput = async () => {
    if (inputText === "") return;
    const paragraphSplit = inputText.split(/\n+/);  // TODO: make safe
    const blocks = paragraphSplit.map((paragraph, i) => {
      const words = paragraph.split(" ").map((word, j) => {
        return <span className="text-block font-l" onClick={(e) => handleBlockClick(j, e.target as HTMLSpanElement)} key={j}>{word}</span>;
      });

      // skip empty paragraphs
      if (words.length === 1 && words[0].props.children === "") return;
      return <p key={i}>{words}</p>
    });
    setOutputBlocks(blocks);
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
            /> : outputBlocks}
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
