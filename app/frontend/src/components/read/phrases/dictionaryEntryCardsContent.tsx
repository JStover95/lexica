import React from "react";
import { IDictionaryEntry, ISeenContent } from "../../../utils/interfaces";
import DictioanryEntryCard from "./dictionaryEntryCard";
import { highlightSubstrings } from "../../../utils/utils";
import DictionaryEntryCardContainer from "./dictionaryCardContainer";

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
        dictionaryEntries.map(({ query, entries, seenContent }, i) => {
          const seen =  seenContent.map((sc, i) =>
            highlightSubstrings(sc.text, sc.indices).map((elem, j) =>
              <div
                key={`seen-content-${i * 10000 + j}`}
                className="mb-2">
                {elem}
              </div>
            )
          )

          const numSeen = seen.reduce((l, r) => l + r.length, 0);

          return (
            <React.Fragment key={`dictionary-entry-${i}`}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-lg">{query}</span>
                {
                  seenContent.length ?
                  <span className="text-sm underline">
                    Seen {numSeen} time{numSeen > 1 && "s"}
                  </span> :
                  ""
                }
              </div>
              {/* <DictionaryEntryCardContainer entries={entries} /> */}
              {seen}
            </React.Fragment>
          );
        })
      }
    </>
  );
}


export default DictionaryEntryCardsContent;
