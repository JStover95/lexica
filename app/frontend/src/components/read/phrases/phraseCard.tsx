import React, { createRef, PropsWithChildren, useEffect } from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import CloseIcon from '@mui/icons-material/Close';

interface IPhraseCardProps extends PropsWithChildren {
  text: string;
  onDeletePhrase: () => void;
}


const PhraseCard: React.FC<IPhraseCardProps> = ({
  text,
  onDeletePhrase,
  children,
}) => {
  return (
    <div className="h-full">
      <div className="flex items-center justify-between sticky top-0 pt-4 border-b border-solid border-black text-lg bg-white">
        <span>{text}</span>
        <div className="p-2 cursor-pointer" onClick={onDeletePhrase}>
          <CloseIcon fontSize="small" />
        </div>
      </div>
      <div className="py-2 overflow-scroll h-[calc(100%-5.75rem)]">
        {children}
      </div>
    </div>
  );
};


export default PhraseCard;
