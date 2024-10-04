import React, { createRef, RefObject, useState } from "react";
import { IDictionaryQuery } from "../../../utils/interfaces";
import SeenContent from "./seenContent";
import DictionaryEntriesContainer from "./dictionaryEntriesContainer";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { useNavigate } from "react-router-dom";

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
  const navigate = useNavigate();

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
    <div key={`seen-content-${i}`} className="mb-2">
      <div onClick={() => navigate("/", { state: { id: sc._id } })}>
        <span className="underline">{sc.title}</span>
      </div>
      {
        sc.sentences.map(({ text, start, stop }, j) =>
          <div key={`seen-content-${i * 10000 + j}`}>
              <span>
                {text.substring(0, start)}
                <b>{text.substring(start, stop + 1)}</b>
                {text.substring(stop + 1)}
              </span>
          </div>
        )
      }
    </div>
  )

  const numSeen = seenContent.reduce((l, r) => l + r.sentences.length, 0);

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
