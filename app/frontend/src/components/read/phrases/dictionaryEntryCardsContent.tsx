import React from "react";
import { IDictionaryEntry, ISeenContent } from "../../../utils/interfaces";
import DictioanryEntryCard from "./dictionaryEntryCard";

function highlightSubstrings(s: string, indices: number[][]) {
  return indices.map(([start, stop], index) => {
    const highlightText = s.slice(start, stop + 1);

    // Find the start of the sentence containing the highlight by going backwards to the previous period
    let sentenceStart = s.lastIndexOf('.', start) + 1;
    // Move the index past any spaces after the period
    while (s[sentenceStart] === ' ') sentenceStart++;

    let sentenceEnd = s.indexOf('.', stop) + 1;

    // Get the surrounding text with highlight centered when possible
    const left = s.slice(sentenceStart, start);
    const right = s.slice(stop + 1, sentenceEnd);

    return (
      <p key={`seen-content-highlight-${index}`} className="mb-2">
          {left}<b>{highlightText}</b>{right}
      </p>
    );
  });
}

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
            <p className="text-lg mb-1">{query}</p>
            {
              seenContent.map((sc, i) =>
                <div key={`seen-content-${i}`} className="text-sm">
                  {highlightSubstrings(sc.text, sc.indices)}
                </div>
              )
            }
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
