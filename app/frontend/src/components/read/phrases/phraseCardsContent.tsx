import React from "react";
import { IDictionaryEntry } from "../../../utils/interfaces";
import PhraseCard from "./phraseCard";
import DictionaryEntryCardsContent from "./dictionaryEntryCardsContent";

interface IPhrase {
  text: string;
  context: string;
  previousText: string;
  active: boolean;
  startIndex: number;
  stopIndex: number;
  dictionaryEntries: IDictionaryEntry[];
}

interface IPhraseCardsContentProps {
  activePhraseIndex: number;
  phrases: IPhrase[];
  handleDeletePhrase: (index: number) => void;
}


const PhraseCardsContent: React.FC<IPhraseCardsContentProps> = ({
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
        <DictionaryEntryCardsContent
          dictionaryEntries={phrases[activePhraseIndex].dictionaryEntries} />
    </PhraseCard>
  );
};


export default PhraseCardsContent;
