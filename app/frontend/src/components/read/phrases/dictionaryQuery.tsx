import React, { useState } from "react";
import { IDictionaryQuery } from "../../../utils/interfaces";
import { highlightSubstrings } from "../../../utils/utils";
import SeenContent from "./seenContent";
import DictionaryEntriesContainer from "./dictionaryEntriesContainer";

interface IDictionaryQueryProps {
  dictionaryQuery: IDictionaryQuery;
}


const DictionaryQuery: React.FC<IDictionaryQueryProps> = ({
  dictionaryQuery,
}) => {
  const [openSeenContent, setOpenSeenContent] = useState(false);
  const { query, entries, seenContent } = dictionaryQuery;

  const handleClickSeenContent = () => setOpenSeenContent(true);
  const handleCloseSeenContent = () => setOpenSeenContent(false);

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
    <>
      <div className="flex items-center justify-between mb-1">
        <span className="text-lg">{query}</span>
        {
          Boolean(seenContent.length) &&
          <span
            onClick={handleClickSeenContent}
            className="text-sm underline">
              Seen {numSeen} time{numSeen > 1 && "s"}
          </span>
        }
      </div>
      <SeenContent
        open={openSeenContent}
        onClose={handleCloseSeenContent}>
          {seen}
      </SeenContent>
      <DictionaryEntriesContainer entries={entries} />
    </>
  );
};


export default DictionaryQuery;
