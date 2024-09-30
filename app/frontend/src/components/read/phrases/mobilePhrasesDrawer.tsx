import React, { createRef, useEffect, useState } from "react";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { IDictionaryEntry } from "../../../utils/interfaces";
import PhraseCard from "./phraseCard";
import { scrollToBottom, scrollToTop } from "../../../utils/utils";

interface IPhrase {
  text: string;
  context: string;
  active: boolean;
  startIndex: number;
  stopIndex: number;
  dictionaryEntries: IDictionaryEntry[] | null;
}

interface IMobilePhrasesDrawerProps {
  phrases: IPhrase[];
  clickedBlockIndex: number;
}


const MobilePhrasesDrawer: React.FC<IMobilePhrasesDrawerProps> = ({
  phrases,
  clickedBlockIndex,
}) => {
  const [open, setOpen] = useState(false);
  const activePhraseRef = createRef<HTMLDivElement>();
  const phraseContainerRef = createRef<HTMLDivElement>();
  const drawerRef = createRef<HTMLDivElement>();

  useEffect(() => {
    if (phraseContainerRef.current && activePhraseRef.current) {
      if (clickedBlockIndex !== -1) {
        scrollToTop(phraseContainerRef.current, activePhraseRef.current);
      } else {
        scrollToBottom(phraseContainerRef.current, activePhraseRef.current);
      }
    }
  }, [phraseContainerRef, activePhraseRef]);

  const handleClickOpen = () => {
    if (drawerRef.current) {
      drawerRef.current.style.height = `calc(${window.innerHeight - 48}px/2)`;
      setOpen(true);
    }
  };

  const handleClickClose = () => {
    if (drawerRef.current) {
      drawerRef.current.style.height = "0px";
      setOpen(false);
    }
  };

  const phraseCards = phrases.map((phrase, i) =>
    <PhraseCard
      key={`phrase-card-${i}`}
      text={phrase.text}
      dictionaryEntries={phrase.dictionaryEntries || []}
      activePhraseRef={
        (
          (
            clickedBlockIndex !== -1
            && phrase.startIndex <= clickedBlockIndex
            && clickedBlockIndex <= phrase.stopIndex
          )
          || clickedBlockIndex === -1 && phrase.active
        ) ?
        activePhraseRef :
        null
      } />
  );

  return (
    <>
      {/* Open drawer button */}
      {
        !open &&
        <button
          className="btn btn-primary w-12 h-12 rounded-4xl sticky bottom-[2rem] left-[calc(50%-1.5rem)] shadow-lg"
          onClick={handleClickOpen}>
            <KeyboardArrowUpIcon fontSize="large" />
        </button>
      }

      <div
        ref={drawerRef}
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
          <div
            ref={phraseContainerRef}
            className="flex flex-col flex-grow bg-white px-8 pt-4 overflow-scroll border-t-2 border-solid border-primary pointer-events-auto">
              {
                phraseCards.length ?
                phraseCards :
                <span className="italic">No phrases selected yet.</span>
              }
          </div>
      </div>
    </>
  );
};


export default MobilePhrasesDrawer;
