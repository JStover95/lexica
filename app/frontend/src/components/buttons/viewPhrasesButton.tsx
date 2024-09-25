import React from "react"
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';


interface IViewPhrasesButtonProps {
  onClick: () => void;
}


const ViewPhrasesButton: React.FC<IViewPhrasesButtonProps> = ({
  onClick
}) => {
  return (
    <div className="flex items-center justify-center bg-primary text-white rounded-4xl shadow-xl fixed w-12 h-12 bottom-6 left-[calc(50vw-1.5rem)]">
      <KeyboardArrowUpIcon sx={{ fontSize: "48px" }} />
    </div>
  );
};


export default ViewPhrasesButton;
