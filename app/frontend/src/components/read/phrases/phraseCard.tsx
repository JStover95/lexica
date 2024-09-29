import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import CloseIcon from '@mui/icons-material/Close';
import DictioanryEntryCard from "./dictionaryEntryCard";

interface IPhraseCardProps {
  text: string;
  dictionaryEntries: IDictionaryEntry[];
}


const PhraseCard: React.FC<IPhraseCardProps> = ({
  text,
  dictionaryEntries,
}) => {
  const dictionaryEntryCards = dictionaryEntries.map((de, i) =>
    <DictioanryEntryCard key={`de-${i}`} dictionaryEntry={de} />
  );

  return (
    <div className="mb-4">
      <div className="flex items-center justify-between mb-2 border-b border-solid border-black text-lg">
        <span>{text}</span>
        <div className="p-2 cursor-pointer">
          <CloseIcon fontSize="small" />
        </div>
      </div>
      {dictionaryEntryCards}
    </div>
  );
};


export default PhraseCard;
