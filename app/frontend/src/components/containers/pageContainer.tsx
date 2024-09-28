import React, { PropsWithChildren } from "react";


const PageContainer: React.FC<PropsWithChildren> = ({ children }) =>
  <div className="my-8 mx-8">
    {children}
  </div>;


export default PageContainer;
