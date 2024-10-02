import React from "react";
import { IDictionaryEntry, ISeenContent } from "../../../utils/interfaces";
import DictioanryEntryCard from "./dictionaryEntryCard";
import { highlightSubstrings } from "../../../utils/utils";

interface IDictionaryEntryCardsContent {
  dictionaryEntries: {
    query: string;
    entries: IDictionaryEntry[];
    seenContent: ISeenContent[];
  }[];
}


const DictionaryEntryCardsContent: React.FC<IDictionaryEntryCardsContent> = ({
  dictionaryEntries,
}) => {
  return (
    <>
      {
        dictionaryEntries.map(({ query, entries, seenContent }, i) =>
          <React.Fragment key={`dictionary-entry-${i}`}>
            <div className="flex items-center justify-between mb-1">
              <span className="text-lg">{query}</span>
              {
                seenContent.length ?
                <span className="text-sm underline">
                  Seen {seenContent.length} time{seenContent.length > 1 && "s"}
                </span> :
                ""
              }
            </div>
            {/* {
              seenContent.map((sc, i) =>
                <div key={`seen-content-${i}`} className="text-sm">
                  {highlightSubstrings(sc.text, sc.indices)}
                </div>
              )
            } */}
            {
              entries.length ?
              entries.map((entry, j) => 
                <DictioanryEntryCard
                  key={`dictionary-entry-${i * 10000 + j}`}
                  dictionaryEntry={entry} />
              ) :
              <p className="text-sm mb-4">
                No dictionary entries found.
              </p>
            }
          </React.Fragment>
        )
      }
    </>
  );
}


export default DictionaryEntryCardsContent;
