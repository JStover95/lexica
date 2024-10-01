import React, { PropsWithChildren } from "react";
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
    <div className="mb-4">
      <div className="flex items-center justify-between sticky top-0 mb-2 pt-4 border-b border-solid border-black text-lg bg-white">
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
