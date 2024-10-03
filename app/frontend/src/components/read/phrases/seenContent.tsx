import React, { createRef, PropsWithChildren, useEffect } from "react";

interface ISeenContentProps extends PropsWithChildren {
  open: boolean;
}


const SeenContent: React.FC<ISeenContentProps> = ({ open, children }) => {
  console.log(open);
  const ref = createRef<HTMLDivElement>();

  useEffect(() => {
    if (ref.current) {
      if (open) {
        const height = [...ref.current.children].reduce(
          (l, r) => l + r.scrollHeight + 8, 0
        );
        ref.current.style.height = `${height}px`;
      } else {
        ref.current.style.height = "0px";
      }
    }
  }, [open, ref]);

  return (
    <div
      className="h-0 overflow-hidden transition-all duration-500"
      ref={ref}>
        {children}
    </div>
  );
};


export default SeenContent;
