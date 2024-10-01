import React, { PropsWithChildren, RefObject } from "react";

interface IPhraseCardCotainerProps extends PropsWithChildren {
  ref?: RefObject<HTMLDivElement>;
}


const PhraseCardContainer: React.FC<IPhraseCardCotainerProps> = ({
  children,
  ref,
}) => {
  return (
    <div
      ref={ref}
      className="flex flex-col flex-grow bg-white px-8 pt-4 overflow-scroll border-t-2 border-solid border-primary pointer-events-auto">
        {children}
    </div>
  );
};


export default PhraseCardContainer;
