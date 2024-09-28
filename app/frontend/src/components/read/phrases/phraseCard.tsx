import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import CloseIcon from '@mui/icons-material/Close';

interface IPhraseCardProps {
  text: string;
  dictionaryEntries: IDictionaryEntry[] | null;
}


const PhraseCard: React.FC<IPhraseCardProps> = ({
  text,
  dictionaryEntries,
}) => {
  return (
    <div className="mb-4">
      <div className="flex items-center justify-between border-b border-solid border-black text-lg">
        <span>{text}</span>
        <div className="p-2 cursor-pointer">
          <CloseIcon fontSize="small" />
        </div>
      </div>
    </div>
  );
};


export default PhraseCard;
