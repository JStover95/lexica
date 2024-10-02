import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import DictioanryEntryCard from "./dictionaryEntryCard";

interface IDictionaryEntryCardContainer {
  entries: IDictionaryEntry[];
}


const DictionaryEntryCardContainer: React.FC<IDictionaryEntryCardContainer> = ({
  entries,
}) => {
  if (!entries.length) {
    return <p className="text-sm mb-4">No dictionary entries found.</p>
  }

  return (
    <>
      {
        entries.map((entry, j) => 
          <DictioanryEntryCard
            key={`dictionary-entry-${j}`}
            dictionaryEntry={entry} />
        )
      }
    </>
  );
}


export default DictionaryEntryCardContainer;
