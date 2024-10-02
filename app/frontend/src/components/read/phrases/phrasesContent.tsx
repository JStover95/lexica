import React from "react";
import { IPhrase } from "../../../utils/interfaces";
import Phrase from "./phrase";

interface IPhrasesContentProps {
  activePhraseIndex: number;
  phrases: IPhrase[];
  handleDeletePhrase: (index: number) => void;
}


const PhrasesContent: React.FC<IPhrasesContentProps> = ({
  activePhraseIndex,
  phrases,
  handleDeletePhrase,
}) => {
  if (!phrases.length) {
    return <span className="italic pt-6">No phrases selected yet.</span>;
  }

  return (
    <Phrase
      text={phrases[activePhraseIndex].text}
      onDeletePhrase={() => handleDeletePhrase(activePhraseIndex)}
      queries={phrases[activePhraseIndex].dictionaryQueries} />
  );
};


export default PhrasesContent;
