import React, { useEffect, useMemo, useState } from "react";
import { dummyText } from "../../utils/dummyData";
import { IDictionaryEntry } from "../../utils/interfaces";
import Block from "../../components/read/block";
import PageContainer from "../../components/containers/pageContainer";
import MobilePhrasesDrawer from "../../components/read/phrases/mobilePhrasesDrawer";

interface IPhrase {
  text: string;
  context: string;
  previousText: string;
  active: boolean;
  startIndex: number;
  stopIndex: number;
  dictionaryEntries: IDictionaryEntry[];
}


const Read: React.FC = () => {
  const [selectedIndices, setSelectedIndices] = useState<Set<number>>(new Set());
  const [phrases, setPhrases] = useState<IPhrase[]>([]);
  const [clickedBlockIndex, setClickedBlockIndex] = useState(-1);

  // Split the text into paragraphs, and within each paragraph, split by words
  const paragraphs = useMemo(() =>
    dummyText.split(/[\n]+/).map((paragraph, pIndex) =>
      paragraph.split(" ").map((word, wIndex) => ({
        text: word,
        index: pIndex * 10000 + wIndex, // Use a unique index by combining paragraph and word indices
        isSentenceFinal: word.endsWith("."),
      }))
    ), [dummyText]);

  useEffect(() => {
    const updatedPhrases = [...phrases];
    updatedPhrases.forEach(async phrase => {
      // If the phrase does not have any new words to query, skip querying the dictionary
      if (phrase.previousText === phrase.text) {
        return;
      };

      // Query only the newly selected words
      let query = phrase.text;
      phrase.previousText.split(" ").forEach(s => {
        query = query.replace(s, "").trim();
      });

      try {
        // Get the inference
        const inference = await fetch(
          process.env.REACT_APP_API_ENDPOINT + "/infer",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "Query": query, "Context": phrase.context })
          }
        );

        const result = await inference.json();
        const entries: IDictionaryEntry[] = result.Result;
        phrase.dictionaryEntries.push(...entries);
        phrase.previousText = phrase.text;
        setPhrases(updatedPhrases);
      } catch (error) {
        console.error(error);
      }
    });
  }, [phrases]);

  const handleClickBlock = (index: number, text: string) => {
    if (selectedIndices.has(index)) {
      setClickedBlockIndex(index);
      return;
    }

    setClickedBlockIndex(-1);

    const updatedSelectedIndices = new Set(selectedIndices);
    const updatedPhrases = [...phrases];
    updatedPhrases.forEach(phrase => phrase.active = false);
    updatedSelectedIndices.add(index);

    // Always create a new phrase on each click of a new block
    const newPhrase: IPhrase = {
      text,
      context: "",
      previousText: "",
      active: true,
      startIndex: index,
      stopIndex: index,
      dictionaryEntries: [],
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
        newPhrase.previousText = leftPhrase.previousText;
        newPhrase.context = leftPhrase.context;
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
        newPhrase.previousText = (
          newPhrase.previousText + " " + rightPhrase.previousText
        ).trim();
        newPhrase.context = rightPhrase.context;
        newPhrase.stopIndex = rightPhrase.stopIndex;
        newPhrase.dictionaryEntries = rightPhrase.dictionaryEntries;
        updatedPhrases.splice(rightPhraseIx, 1);
      }
    }

    if (newPhrase.context === "") {
      const p = paragraphs[Math.floor(index / 10000)];
      let i = index % 10000;
      newPhrase.context = p[i].text;
      // TODO: Handle quotes
      while (i > 0 && !p[i - 1].text.endsWith(".")) {
        newPhrase.context = p[i - 1].text + " " + newPhrase.context;
        i--;
      }
      i = index % 10000;
      while (i < p.length - 1 && !p[i].text.endsWith(".")) {
        newPhrase.context = newPhrase.context + " " + p[i + 1].text;
        i++;
      }
    }

    // Add the new phrase
    updatedPhrases.push(newPhrase);

    // Sort phrases by start index
    updatedPhrases.sort((a, b) => a.startIndex - b.startIndex);

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
                    active={
                      !word.isSentenceFinal &&
                      shouldUnderlineSpace(word.index, word.index + 1)
                    }>
                      {" "}
                  </Block>
                )}
              </React.Fragment>
            ))}
          </div>
        ))}
      </PageContainer>

      {/* Mobile phrases drawer */}
      <MobilePhrasesDrawer
        phrases={phrases}
        clickedBlockIndex={clickedBlockIndex} />
    </>
  );
};

export default Read;
