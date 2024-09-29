import React from "react";
import { ISense } from "../../../utils/interfaces";

interface ISenseCardProps {
  sense: ISense;
}


const SenseCard: React.FC<ISenseCardProps> = ({ sense }) => {
  // For now hard code English only
  const equivalent = sense.equivalents?.filter(eq => eq.equivalentLanguage == "영어")[0];

  if (!equivalent) {
    return (
      <div className="mb-2">
        <span className="text-sm">{sense.definition}</span>
      </div>
    );
  }

  return (
    <div className="mb-1">
      <p className="text-sm">{equivalent.equivalent}</p>
      <p className="text-sm">{sense.definition}</p>
      <p className="text-sm">{equivalent.definition}</p>
    </div>
  );
}


export default SenseCard;
