import React, { createRef, PropsWithChildren, useEffect } from "react";

interface ISeenContentProps extends PropsWithChildren {
  open: boolean;
  onClose: () => void;
}


const SeenContent: React.FC<ISeenContentProps> = ({
  open,
  onClose,
  children,
}) => {
  const ref = createRef<HTMLDivElement>();

  useEffect(() => {
    if (open && ref.current) {
      const height = [...ref.current.children].reduce(
        (l, r) => l + r.scrollHeight, 0
      );
      ref.current.style.height = `${height}px`;
    }
  }, [open, ref]);

  const handleClickClose = () => {
    if (ref.current) {
      onClose();
      ref.current.style.height = "0px";
    }
  }

  return (
    <div
      className="h-0 overflow-hidden transition-all duration-500"
      ref={ref}>
        <span onClick={handleClickClose}>Close</span>
        {children}
    </div>
  );
};


export default SeenContent;
