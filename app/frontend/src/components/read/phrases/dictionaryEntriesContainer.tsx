import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import DictioanryEntry from "./dictionaryEntry";

interface IDictionaryEntriesContainerProps {
  entries: IDictionaryEntry[];
}


const DictionaryEntriesContainer: React.FC<IDictionaryEntriesContainerProps> = ({
  entries,
}) => {
  if (!entries.length) {
    return <p className="text-sm mb-4">No dictionary entries found.</p>
  }

  return (
    <>
      {
        entries.map((entry, j) => 
          <DictioanryEntry
            key={`dictionary-entry-${j}`}
            dictionaryEntry={entry} />
        )
      }
    </>
  );
}


export default DictionaryEntriesContainer;
