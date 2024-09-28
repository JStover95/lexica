import React, { createRef } from "react";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { IDictionaryEntry } from "../../../utils/interfaces";
import PhraseCard from "./phraseCard";

interface IPhrase {
  text: string;
  startIndex: number;
  stopIndex: number;
  dictionaryEntries: IDictionaryEntry[] | null;
}

interface IMobilePhrasesDrawer {
  phrases: IPhrase[];
}


const MobilePhrasesDrawer: React.FC<IMobilePhrasesDrawer> = ({
  phrases
}) => {
  const ref = createRef<HTMLDivElement>();

  const handleClickOpen = () => {
    if (ref.current) {
      ref.current.style.height = "18rem";
    }
  };

  const handleClickClose = () => {
    if (ref.current) {
      ref.current.style.height = "0px";
    }
  };

  const phraseCards = phrases.map((phrase, i) =>
    <PhraseCard
      key={`phrase-card-${i}`}
      text={phrase.text}
      dictionaryEntries={phrase.dictionaryEntries} />
  );

  return (
    <>
      {/* Open drawer button */}
      <button
        className="btn btn-primary w-12 h-12 rounded-4xl sticky bottom-[2rem] left-[calc(50%-1.5rem)] shadow-lg"
        onClick={handleClickOpen}>
          <KeyboardArrowUpIcon fontSize="large" />
      </button>

      <div
        ref={ref}
        className="flex flex-col sticky bottom-0 z-10 h-0 overflow-hidden transition-all duration-500 pointer-events-none">

          {/* Close drawer button */}
          <div className="flex justify-center">
            <div
              className="flex items-center justify-center w-20 h-8 rounded-t-lg bg-primary text-white pointer-events-auto cursor-pointer hover:brightness-[110%] active:brightness-[110%]"
              onClick={handleClickClose}>
                <KeyboardArrowDownIcon fontSize="large" />
            </div>
          </div>

          {/* Phrases list */}
          <div className="flex flex-col flex-grow bg-white px-8 pt-4 overflow-scroll border-t-2 border-solid border-primary pointer-events-auto">
            {phraseCards}
          </div>
      </div>
    </>
  );
};


export default MobilePhrasesDrawer;
