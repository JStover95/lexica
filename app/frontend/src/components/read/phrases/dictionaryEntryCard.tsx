import React, { useState } from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import SenseCard from "./senseCard";

interface IDictionaryEntryCardProps {
  dictionaryEntry: IDictionaryEntry;
  onClickSelectDefinition: () => void;
  onSelectDefinition: () => void;
}


const DictioanryEntryCard: React.FC<IDictionaryEntryCardProps> = ({
  dictionaryEntry,
  onClickSelectDefinition,
  onSelectDefinition,
}) => {
  const [selectingDefinition, setSelectingDefinition] = useState(false);

  const handleClickSelectDefinition = () => {
    onClickSelectDefinition();
    setSelectingDefinition(true);
  };

  const sensesWithNums = dictionaryEntry.senses.map((sense, i) => (
    { sense, num: i + 1 }
  ));

  let senseCards;
  if (selectingDefinition) {
    senseCards = sensesWithNums.map((sense, i) =>
      <SenseCard
        key={`sense-card-${i}`}
        sense={sense.sense}
        senseNum={sense.num} />
    );
  } else {
    const topSenseWithNum = sensesWithNums.sort(
      (l, r) => (l.sense.rank || 0) - (r.sense.rank || 0)
    )[0];
    senseCards = [
      <SenseCard sense={topSenseWithNum.sense} senseNum={topSenseWithNum.num} />
    ];
  }

  return (
    <>
      <div className="mb-4">
        <div className="flex items-center mb-1">
          <span className="text-lg font-bold mr-2">{dictionaryEntry.writtenForm}</span>
          <span className="text-sm">{dictionaryEntry.partOfSpeech}</span>
        </div>
        {senseCards}
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
