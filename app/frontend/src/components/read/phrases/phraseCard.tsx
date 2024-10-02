import React, { createRef, PropsWithChildren, useEffect } from "react";
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
  const headerRef = createRef<HTMLDivElement>();
  const sensesListRef = createRef<HTMLDivElement>();

  useEffect(() => {
    if (headerRef.current && sensesListRef.current) {
      const headerHeight = headerRef.current.scrollHeight;
      sensesListRef.current.style.height =
        `calc(100% - ${headerHeight + 32}px)`;
    }
  }, [headerRef, sensesListRef])

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
        ref={sensesListRef}
        className="p-2 overflow-scroll">
          {children}
      </div>
    </div>
  );
};


export default PhraseCard;
