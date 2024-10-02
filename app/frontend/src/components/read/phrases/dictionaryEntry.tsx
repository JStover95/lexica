import React, { createRef, useEffect, useState } from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import Sense from "./sense";

interface IDictionaryEntryProps {
  dictionaryEntry: IDictionaryEntry;
}


const DictioanryEntryCard: React.FC<IDictionaryEntryProps> = ({
  dictionaryEntry,
}) => {
  const [selectingDefinition, setSelectingDefinition] = useState(false);
  const [selectedDefinitionIndex, setSelectedDefinitionIndex] = useState(-1);

  const handleClickSelectDefinition = () => {
    setSelectingDefinition(true);
  };

  const handleSelectDefinition = (index: number) => {
    setSelectedDefinitionIndex(index);
    setSelectingDefinition(false);
  }

  const sensesWithNums = dictionaryEntry.senses.map((sense, i) => (
    { sense, num: i + 1 }
  ));

  let topSenseWithNum;
  if (selectedDefinitionIndex !== -1) {
    topSenseWithNum = sensesWithNums[selectedDefinitionIndex];
  } else {
    topSenseWithNum = [...sensesWithNums].sort(
      (l, r) => (l.sense.rank || 0) - (r.sense.rank || 0)
    )[0];
  }

  let senseCards;
  if (selectingDefinition) {
    senseCards = sensesWithNums.map((sense, i) =>
      <Sense
        key={`sense-card-${i}`}
        sense={sense.sense}
        senseNum={sense.num}
        onClick={() => handleSelectDefinition(i)} />
    );
  } else {
    senseCards = [
      <Sense
        key={"sense-card-0"}
        sense={topSenseWithNum.sense}
        senseNum={topSenseWithNum.num} />
    ];
  }

  return (
    <>
      <div className="mb-4">
        <div className="flex items-center justify-between mb-1">
          <div className="flex items-center">
            <span className="text-lg font-bold mr-2">{dictionaryEntry.writtenForm}</span>
            <span className="text-sm">{dictionaryEntry.partOfSpeech}</span>
          </div>
        </div>
        {
          selectingDefinition &&
          <>
            <p className="text-sm font-bold pt-2">Previous definition</p>
            <Sense
              key={"sense-card-0"}
              sense={topSenseWithNum.sense}
              senseNum={topSenseWithNum.num}
              onClick={() => handleSelectDefinition(selectedDefinitionIndex)} />
            <p className="text-sm font-bold pt-2">Select a new definition</p>
          </>
        }
        {
          selectingDefinition ?
          senseCards.filter((_, i) => i !== selectedDefinitionIndex) :
          senseCards
        }
        {
          (dictionaryEntry.senses.length > 1 && !selectingDefinition) &&
          <span
            onClick={handleClickSelectDefinition}
            className="text-sm underline cursor-pointer">
              Choose a different definition...
          </span>
        }
      </div>
    </>
  );
};


export default DictioanryEntryCard;
