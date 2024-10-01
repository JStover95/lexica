import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import PhraseCard from "./phraseCard";
import DictionaryEntryCardContent from "./dictionaryEntryCardContent";

interface IPhrase {
  text: string;
  context: string;
  previousText: string;
  active: boolean;
  startIndex: number;
  stopIndex: number;
  dictionaryEntries: IDictionaryEntry[];
}

interface IPhraseCardContentProps {
  activePhraseIndex: number;
  phrases: IPhrase[];
  handleDeletePhrase: (index: number) => void;
}


const PhraseCardContent: React.FC<IPhraseCardContentProps> = ({
  activePhraseIndex,
  phrases,
  handleDeletePhrase,
}) => {
  if (!phrases.length) {
    return <span className="italic pt-6">No phrases selected yet.</span>;
  }

  return (
    <PhraseCard
      text={phrases[activePhraseIndex].text}
      onDeletePhrase={() => handleDeletePhrase(activePhraseIndex)}>
        <DictionaryEntryCardContent
          dictionaryEntries={phrases[activePhraseIndex].dictionaryEntries} />
    </PhraseCard>
  );
};


export default PhraseCardContent;
