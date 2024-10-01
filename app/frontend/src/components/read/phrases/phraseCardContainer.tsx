import React, { PropsWithChildren } from "react";

const PhraseCardContainer: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <div className="flex flex-col flex-grow bg-white px-8 overflow-scroll border-t-2 border-solid border-primary pointer-events-auto">
        {children}
    </div>
  );
};


export default PhraseCardContainer;
