import React, { createRef, PropsWithChildren, useEffect } from "react";
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
  const headerRef = createRef<HTMLDivElement>();
  const queriesContainerRef = createRef<HTMLDivElement>();
  const lastQueryRef = createRef<HTMLDivElement>();

  useEffect(() => {
    if (queriesContainerRef.current && lastQueryRef.current) {
      scrollToTop(queriesContainerRef.current, lastQueryRef.current);
    }
  }, [queriesContainerRef, lastQueryRef]);

  useEffect(() => {
    if (headerRef.current && queriesContainerRef.current) {
      const headerHeight = headerRef.current.scrollHeight;
      queriesContainerRef.current.style.height =
        `calc(100% - ${headerHeight + 32}px)`;
    }
  }, [headerRef, queriesContainerRef])

  return (
    <div className="h-full">
      <div
        ref={headerRef}
        className="flex items-center justify-between sticky top-0 pt-4 border-b border-solid border-black text-lg bg-white">
          <span>{text}</span>
          <div className="p-2 cursor-pointer" onClick={onDeletePhrase}>
            <CloseIcon fontSize="small" />
          </div>
      </div>
      <div
        ref={queriesContainerRef}
        className="p-2 overflow-scroll">
          {
            queries.map((dq, i) =>
              <DictionaryQuery
                key={i}
                dictionaryQuery={dq}
                lastQueryRef={i === queries.length - 1 ? lastQueryRef : null} />
            )
          }
      </div>
    </div>
  );
};


export default Phrase;
