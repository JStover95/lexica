import React from "react";
import { IPhrase } from "../../../utils/interfaces";
import Phrase from "./phrase";
import DictionaryQuery from "./dictionaryQuery";

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
      onDeletePhrase={() => handleDeletePhrase(activePhraseIndex)}>
        {
          phrases[activePhraseIndex].dictionaryQueries.map((dq, i) =>
            <DictionaryQuery key={i} dictionaryQuery={dq} />
          )
        }
    </Phrase>
  );
};


export default PhrasesContent;
