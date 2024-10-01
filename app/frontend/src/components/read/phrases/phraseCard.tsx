import React, { PropsWithChildren, RefObject } from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import CloseIcon from '@mui/icons-material/Close';

interface IPhraseCardProps extends PropsWithChildren {
  text: string;
  phraseCardRef: RefObject<HTMLDivElement>;
  onDeletePhrase: () => void;
}


const PhraseCard: React.FC<IPhraseCardProps> = ({
  text,
  phraseCardRef,
  onDeletePhrase,
  children,
}) => {

  return (
    <div ref={phraseCardRef} className="mb-4">
      <div className="flex items-center justify-between mb-2 border-b border-solid border-black text-lg">
        <span>{text}</span>
        <div className="p-2 cursor-pointer" onClick={onDeletePhrase}>
          <CloseIcon fontSize="small" />
        </div>
      </div>
      {children}
    </div>
  );
};


export default PhraseCard;
