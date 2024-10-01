import React from "react";
import { ISense } from "../../../utils/interfaces";

interface ISenseCardProps {
  sense: ISense;
  senseNum: number;
}


const SenseCard: React.FC<ISenseCardProps> = ({ sense, senseNum }) => {
  // For now hard code English only
  const equivalent = sense.equivalents?.filter(eq => eq.equivalentLanguage == "영어")[0];

  if (!equivalent) {
    return (
      <ol className="mb-2 list-decimal pl-8" start={senseNum}>
        <li>
          <span className="text-sm">{sense.definition}</span>
        </li>
      </ol>
    );
  }

  return (
    <ol className="mb-1 list-decimal pl-8" start={senseNum}>
      <li>
        <p className="text-sm">{equivalent.equivalent}</p>
        <p className="text-sm">{sense.definition}</p>
        <p className="text-sm">{equivalent.definition}</p>
      </li>
    </ol>
  );
}


export default SenseCard;
