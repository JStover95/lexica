import React, { createRef, RefObject, useState } from "react";
import { IDictionaryQuery } from "../../../utils/interfaces";
import { highlightSubstrings } from "../../../utils/utils";
import SeenContent from "./seenContent";
import DictionaryEntriesContainer from "./dictionaryEntriesContainer";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

interface IDictionaryQueryProps {
  dictionaryQuery: IDictionaryQuery;
  lastQueryRef?: RefObject<HTMLDivElement> | null;
}


const DictionaryQuery: React.FC<IDictionaryQueryProps> = ({
  dictionaryQuery,
  lastQueryRef,
}) => {
  const [openSeenContent, setOpenSeenContent] = useState(false);
  const { query, entries, seenContent } = dictionaryQuery;
  const arrowRef = createRef<HTMLDivElement>();

  const handleClickSeenContent = () => {
    if (arrowRef.current) {
      if (openSeenContent) {
        arrowRef.current.style.transform = "rotate(0deg)";
      } else {
        arrowRef.current.style.transform = "rotate(180deg)";
      }
    }
    setOpenSeenContent(!openSeenContent);
  };

  const seen = seenContent.map((sc, i) =>
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
    <div ref={lastQueryRef}>
      <div className="flex items-center justify-between mb-1">
        <span className="text-lg">{query}</span>
        {
          Boolean(seenContent.length) &&
          <div
            onClick={handleClickSeenContent}
            className="flex items-center">
              <span className="text-sm underline">
                  Seen {numSeen} time{numSeen > 1 && "s"}
              </span>
              <div
                ref={arrowRef}
                className="flex items-center transition-all duration-300">
                  <KeyboardArrowDownIcon sx={{ fontSize: "20px" }} />
              </div>
          </div>
        }
      </div>
      <SeenContent open={openSeenContent}>
          {seen}
      </SeenContent>
      <DictionaryEntriesContainer entries={entries} />
    </div>
  );
};


export default DictionaryQuery;
