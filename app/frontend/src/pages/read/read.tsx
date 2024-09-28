import React, { useMemo, useState } from "react";
import { dummyText } from "../../utils/dummyData";
import { IDictionaryEntry } from "../../utils/interfaces";
import Block from "../../components/read/block";
import PageContainer from "../../components/containers/pageContainer";
import MobilePhrasesDrawer from "../../components/read/phrases/mobilePhrasesDrawer";

interface IPhrase {
  text: string;
  startIndex: number;
  stopIndex: number;
  dictionaryEntries: IDictionaryEntry[] | null;
}


const Read: React.FC = () => {
  const [selectedIndices, setSelectedIndices] = useState<Set<number>>(new Set());
  const [phrases, setPhrases] = useState<IPhrase[]>([]);

  // Split the text into paragraphs, and within each paragraph, split by words
  const paragraphs = useMemo(() =>
    dummyText.split(/[\n]+/).map((paragraph, pIndex) =>
      paragraph.split(" ").map((word, wIndex) => ({
        text: word,
        index: pIndex * 10000 + wIndex, // Use a unique index by combining paragraph and word indices
      }))
    ), [dummyText]);

  const handleClickBlock = (index: number, text: string) => {
    if (selectedIndices.has(index)) {
      return;
    }

    const updatedSelectedIndices = new Set(selectedIndices);
    const updatedPhrases = [...phrases];
    updatedSelectedIndices.add(index);

    // Always create a new phrase on each click of a new block
    const newPhrase: IPhrase = {
      text,
      startIndex: index,
      stopIndex: index,
      dictionaryEntries: null,
    };

    // Check for an adjacent block to the left
    if (selectedIndices.has(index - 1)) {

      // Get the phrase that contains the adjacent block
      const leftPhraseIx = updatedPhrases.findIndex(
        phrase => phrase.stopIndex === index - 1
      );
      const leftPhrase = updatedPhrases[leftPhraseIx];

      // If the adjacent block is not the end of a sentence
      if (!leftPhrase.text.endsWith(".")) {

        // Merge the adjacent phrase with the new phrase
        newPhrase.text = leftPhrase.text + " " + newPhrase.text;
        newPhrase.startIndex = leftPhrase.startIndex;
        newPhrase.dictionaryEntries = leftPhrase.dictionaryEntries;

        // Delete the adjacent phrase
        updatedPhrases.splice(leftPhraseIx, 1);
      }
    }

    // Check for an adjacent block to the right as before
    if (selectedIndices.has(index + 1)) {
      const rightPhraseIx = updatedPhrases.findIndex(
        phrase => phrase.startIndex === index + 1
      );
      const rightPhrase = updatedPhrases[rightPhraseIx];

      // If the current block is not the end of a sentence
      if (!text.endsWith(".")) {
        newPhrase.text = newPhrase.text + " " + rightPhrase.text;
        newPhrase.stopIndex = rightPhrase.stopIndex;
        newPhrase.dictionaryEntries = rightPhrase.dictionaryEntries;
        updatedPhrases.splice(rightPhraseIx, 1);
      }
    }

    // Add the new phrase
    updatedPhrases.push(newPhrase);

    // Sort phrases by start index
    updatedPhrases.sort((a, b) => {
      if (a.startIndex > b.startIndex) return 1;
      else if (a.startIndex < b.startIndex) return -1;
      return 0;
    });

    setSelectedIndices(updatedSelectedIndices);
    setPhrases(updatedPhrases);
  };

  const shouldUnderlineSpace = (prevIndex: number, nextIndex: number) => {
    return selectedIndices.has(prevIndex) && selectedIndices.has(nextIndex);
  };

  return (
    <>
      <PageContainer>
        {/* Reading view */}
        {paragraphs.map((paragraph, i) => (
          <div key={i} className="mb-4">
            {paragraph.map((word, j) => (
              <React.Fragment key={word.index}>
                <Block
                  active={selectedIndices.has(word.index)}
                  onClick={() => handleClickBlock(word.index, word.text)}>
                    {word.text}
                </Block>
                {j < paragraph.length - 1 && (
                  <Block
                    active={shouldUnderlineSpace(word.index, word.index + 1)}>
                      {" "}
                  </Block>
                )}
              </React.Fragment>
            ))}
          </div>
        ))}
      </PageContainer>

      {/* Mobile phrases drawer */}
      <MobilePhrasesDrawer phrases={phrases} />
    </>
  );
};

export default Read;
