import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import DictioanryEntryCard from "./dictionaryEntryCard";

interface IDictionaryEntryCardContent {
  dictionaryEntries: IDictionaryEntry[];
}


const DictionaryEntryCardContent: React.FC<IDictionaryEntryCardContent> = ({
  dictionaryEntries,
}) => {
  if (!dictionaryEntries.length) {
    return <span className="italic">No dictionary entries found.</span>
  }

  const dictionaryEntryCards = dictionaryEntries.map((de, i) =>
    <DictioanryEntryCard
      key={`dictionary-entry-${i}`}
      dictionaryEntry={de} />
  );

  return (
    <>
      {dictionaryEntryCards}
    </>
  );
}


export default DictionaryEntryCardContent;
