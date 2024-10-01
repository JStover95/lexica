import React, { PropsWithChildren, RefObject } from "react";

interface IPhraseCardCotainerProps extends PropsWithChildren {
  phraseContainerRef?: RefObject<HTMLDivElement>;
}


const PhraseCardContainer: React.FC<IPhraseCardCotainerProps> = ({
  children,
  phraseContainerRef,
}) => {
  return (
    <div
      ref={phraseContainerRef}
      className="flex flex-col flex-grow bg-white px-8 overflow-scroll border-t-2 border-solid border-primary pointer-events-auto">
        {children}
    </div>
  );
};


export default PhraseCardContainer;
