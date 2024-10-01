import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import SenseCard from "./senseCard";

interface IDictionaryEntryCardProps {
  dictionaryEntry: IDictionaryEntry;
}


const DictioanryEntryCard: React.FC<IDictionaryEntryCardProps> = ({
  dictionaryEntry
}) => {
  const sensesWithNums = dictionaryEntry.senses.map((sense, i) => (
    { sense, num: i + 1 }
  ));

  const senseWithNum = sensesWithNums.sort(
    (l, r) => (l.sense.rank || 0) - (r.sense.rank || 0)
  )[0];

  return (
    <>
      <div className="mb-4">
        <div className="flex items-center mb-1">
          <span className="text-lg font-bold mr-2">{dictionaryEntry.writtenForm}</span>
          <span className="text-sm">{dictionaryEntry.partOfSpeech}</span>
        </div>
        <SenseCard sense={senseWithNum.sense} senseNum={senseWithNum.num} />
        {
          dictionaryEntry.senses.length > 1 &&
          <span className="text-sm underline">Choose a different definition...</span>
        }
      </div>
    </>
  );
};


export default DictioanryEntryCard;
