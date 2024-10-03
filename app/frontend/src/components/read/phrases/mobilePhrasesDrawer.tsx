import React, { createRef, PropsWithChildren, useCallback, useEffect, useState } from "react";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';

interface IMobilePhraseDrawer extends PropsWithChildren {
  open: boolean;
  onOpen: () => void;
  onClose: () => void;
}


const MobilePhrasesDrawer: React.FC<IMobilePhraseDrawer> = ({
  open,
  onOpen,
  onClose,
  children,
}) => {
  const drawerRef = createRef<HTMLDivElement>();

  const handleClickOpen = useCallback(() => {
    if (drawerRef.current) {
      drawerRef.current.style.height = `calc(${window.innerHeight - 16}px / 2)`;
      onOpen();
    }
  }, [drawerRef, onOpen]);

  const handleClickClose = useCallback(() => {
    if (drawerRef.current) {
      drawerRef.current.style.height = "0px";
      onClose();
    }
  }, [drawerRef, onClose]);

  useEffect(() => {
    if (open) {
      handleClickOpen();
    } else {
      handleClickClose();
    }
  }, [handleClickClose, handleClickOpen, open]);

  return (
    <>
      {/* Open drawer button */}
      {
        !open &&
        <button
          className="btn btn-primary w-12 h-12 rounded-4xl sticky bottom-[2rem] left-[calc(50%-1.5rem)] shadow-lg"
          onClick={handleClickOpen}>
            <KeyboardArrowUpIcon fontSize="large" />
        </button>
      }

      {/* Phrases */}
      <div
        ref={drawerRef}
        className="flex flex-col sticky bottom-0 z-10 h-0 overflow-hidden transition-all duration-500 pointer-events-none">
          {/* Close drawer button */}
          <div className="flex justify-center border-b-2 border-primary">
            <div
              className="flex items-center justify-center w-20 h-8 rounded-t-lg bg-primary text-white pointer-events-auto cursor-pointer hover:brightness-[110%] active:brightness-[110%]"
              onClick={handleClickClose}>
                <KeyboardArrowDownIcon fontSize="large" />
            </div>
          </div>
          {children}
      </div>
    </>
  );
};


export default MobilePhrasesDrawer;
