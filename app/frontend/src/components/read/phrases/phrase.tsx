import React, { createRef, PropsWithChildren, useEffect, useRef, useState } from "react";
import CloseIcon from '@mui/icons-material/Close';
import { IDictionaryQuery } from "../../../utils/interfaces";
import DictionaryQuery from "./dictionaryQuery";
import { scrollToTop } from "../../../utils/utils";

interface IPhraseProps {
  text: string;
  queries: IDictionaryQuery[];
  onDeletePhrase: () => void;
}


const Phrase: React.FC<IPhraseProps> = ({
  text,
  queries,
  onDeletePhrase
}) => {
  const [scroll, setScroll] = useState(false);
  const queriesContainerRef = createRef<HTMLDivElement>();
  const lastQueryRef = createRef<HTMLDivElement>();
  const prevText = useRef<string | null>(null);
  const prevQueries = useRef<IDictionaryQuery[] | null>(null);

  useEffect(() => {
    if (prevText.current === null || prevQueries.current === null) {
      prevText.current = "";
      prevQueries.current = [];
    } else {
      setScroll(prevQueries.current === queries || prevText.current === text);
      prevQueries.current = queries;
      prevText.current = text;
    }
  }, [text, queries]);

  useEffect(() => {
    if (queriesContainerRef.current && lastQueryRef.current) {
      if (scroll) {
        scrollToTop(queriesContainerRef.current, lastQueryRef.current);
      } else {
        queriesContainerRef.current.scrollTo({ top: 0 });
      }
    }
  }, [queriesContainerRef, lastQueryRef]);

  return (
    <div
      ref={queriesContainerRef}
      className="px-8 h-[calc(100%-32px)] overflow-scroll">
        <div
          className="flex items-center pt-4 pb-2 mb-4 justify-between border-b border-solid border-black text-lg bg-white">
            <span>{text}</span>
            <div className="cursor-pointer" onClick={onDeletePhrase}>
              <CloseIcon fontSize="small" />
            </div>
        </div>
        {
          queries.map((dq, i) =>
            <DictionaryQuery
              key={i}
              dictionaryQuery={dq}
              lastQueryRef={i === queries.length - 1 ? lastQueryRef : null} />
          )
        }
    </div>
  );
};


export default Phrase;
