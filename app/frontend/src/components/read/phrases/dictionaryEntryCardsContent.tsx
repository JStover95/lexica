import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import DictioanryEntryCard from "./dictionaryEntryCard";

interface IDictionaryEntryCardsContent {
  dictionaryEntries: { query: string; entries: IDictionaryEntry[]}[];
}


const DictionaryEntryCardsContent: React.FC<IDictionaryEntryCardsContent> = ({
  dictionaryEntries,
}) => {
  return (
    <>
      {
        dictionaryEntries.map(({ query, entries }, i) =>
          <React.Fragment key={`dictionary-entry-${i}`}>
            <p className="text-lg mb-1">{query}</p>
            {
              entries.length ?
              entries.map((entry, j) => 
                <DictioanryEntryCard
                  key={`dictionary-entry-${i * 10000 + j}`}
                  dictionaryEntry={entry} />
              ) :
              <span className="text-sm">
                No dictionary entries found.
              </span>
            }
          </React.Fragment>
        )
      }
    </>
  );
}


export default DictionaryEntryCardsContent;
