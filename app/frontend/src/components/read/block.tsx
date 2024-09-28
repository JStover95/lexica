import React, { PropsWithChildren } from "react";

interface IBlockProps extends PropsWithChildren {
  active: boolean;
  onClick?: () => void;
}


const Block: React.FC<IBlockProps> = ({
  active,
  onClick,
  children
}) =>
  <span
    className={"text-block text-xl" + (active ? " text-block-0" : "")}
    onClick={onClick}>
      {children}
  </span>


export default Block;
