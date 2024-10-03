import React, { PropsWithChildren } from "react";

const PhrasesContainer: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <div className="flex flex-col h-full flex-grow bg-white pointer-events-auto">
        {children}
    </div>
  );
};


export default PhrasesContainer;
