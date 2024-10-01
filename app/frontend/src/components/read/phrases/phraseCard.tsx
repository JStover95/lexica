import React, { RefObject } from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import CloseIcon from '@mui/icons-material/Close';
import DictioanryEntryCard from "./dictionaryEntryCard";

interface IPhraseCardProps {
  text: string;
  dictionaryEntries: IDictionaryEntry[];
  activePhraseRef: RefObject<HTMLDivElement> | null;
  onDeletePhrase: () => void;
  onClickSelectDefinition: () => void;
  onSelectDefinition: () => void;
}


const PhraseCard: React.FC<IPhraseCardProps> = ({
  text,
  dictionaryEntries,
  activePhraseRef,
  onDeletePhrase,
  onClickSelectDefinition,
  onSelectDefinition,
}) => {
  const dictionaryEntryCards = dictionaryEntries.map((de, i) =>
    <DictioanryEntryCard
      key={`de-${i}`}
      dictionaryEntry={de}
      onClickSelectDefinition={onClickSelectDefinition}
      onSelectDefinition={onSelectDefinition} />
  );

  return (
    <div ref={activePhraseRef} className="mb-4">
      <div className="flex items-center justify-between mb-2 border-b border-solid border-black text-lg">
        <span>{text}</span>
        <div className="p-2 cursor-pointer" onClick={onDeletePhrase}>
          <CloseIcon fontSize="small" />
        </div>
      </div>
      {
        dictionaryEntryCards.length ?
        dictionaryEntryCards :
        <span className="italic">No dictionary entries found</span>
      }
    </div>
  );
};


export default PhraseCard;
