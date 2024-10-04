import React, { useEffect, useMemo, useState } from "react";
import { dummyText } from "../utils/dummyData";
import { IContent, IInferResponseBody, IPhrase, ISeenContentResponseBody } from "../utils/interfaces";
import Block from "../components/read/block";
import PageContainer from "../components/containers/pageContainer";
import MobilePhrasesDrawer from "../components/read/phrases/mobilePhrasesDrawer";
import PhrasesContent from "../components/read/phrases/phrasesContent";
import PhrasesContainer from "../components/read/phrases/phrasesContainer";
import { Location, useLocation } from "react-router-dom";


const Read: React.FC = () => {
  const [text, setText] = useState<string | null>(null);
  const [selectedIndices, setSelectedIndices] = useState<Set<number>>(new Set());
  const [phrases, setPhrases] = useState<IPhrase[]>([]);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [activePhraseIndex, setActivePhraseIndex] = useState(-1);
  const location: Location<{ id: string }> | null = useLocation();

  const getContent = async (id: string): Promise<IContent | null> => {
    const query = `
      query getContentById($id: String!) {
        content_by_id(id: $id) {
          id
          title
          text
        }
      }
    `;
  
    const variables = { id };
  
    try {
      const url = process.env.REACT_APP_API_ENDPOINT + "/graphql";
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
          variables,
        }),
      });
  
      const result = await response.json();
  
      if (response.ok && result.data) {
        return result.data.content_by_id;
      } else {
        console.error("Error fetching content:", result.errors);
        return null;
      }
    } catch (error) {
      console.error("Error fetching content:", error);
      return null;
    }
  };

  useEffect(() => {
    if (location.state?.id) {
      console.log(location.state.id);
    }
  }, [location]);

  // Split the text into paragraphs, and within each paragraph, split by words
  const paragraphs = useMemo(() =>
    dummyText.split(/[\n]+/).map((paragraph, pIndex) =>
      paragraph.split(" ").map((word, wIndex) => ({
        text: word,
        index: pIndex * 10000 + wIndex, // Use a unique index by combining paragraph and word indices
        isSentenceFinal: word.endsWith("."),
      }))
    ), []);

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
        const inferencePromise = fetch(
          process.env.REACT_APP_API_ENDPOINT + "/infer",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "Query": query, "Context": phrase.context })
          }
        );

        const url = new URL(process.env.REACT_APP_API_ENDPOINT + "/seen-content")
        const params = new URLSearchParams();
        params.append("q", query);
        url.search = params.toString();
        const contentPromise = fetch(url);

        const [inference, content] = await Promise.all(
          [inferencePromise, contentPromise]
        )

        const inferenceResult: IInferResponseBody = await inference.json();
        const contentResult: ISeenContentResponseBody = await content.json();
        console.log(contentResult);
        const entries = inferenceResult.Result;
        const seenContent = contentResult.Result;
        phrase.dictionaryQueries.push({ query, entries, seenContent });
        phrase.previousText = phrase.text;
        setPhrases(updatedPhrases);
      } catch (error) {
        console.error(error);
      }
    });
  }, [phrases]);

  const handleClickBlock = (index: number, text: string) => {
    setDrawerOpen(true);

    if (selectedIndices.has(index)) {
      const phraseIndex = phrases.findIndex(phrase =>
        phrase.startIndex <= index && index <= phrase.stopIndex
      );
      setActivePhraseIndex(phraseIndex);
      return;
    }

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
      dictionaryQueries: [],
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
        newPhrase.dictionaryQueries = leftPhrase.dictionaryQueries;

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
        newPhrase.dictionaryQueries = [
          ...newPhrase.dictionaryQueries, ...rightPhrase.dictionaryQueries
        ];
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

    updatedPhrases.push(newPhrase);
    setSelectedIndices(updatedSelectedIndices);
    setPhrases(updatedPhrases);
    setActivePhraseIndex(updatedPhrases.length - 1);
  };

  const handleDeletePhrase = (index: number) => {
    const updatedPhrases = [...phrases];
    const updatedSelectedIndices = new Set(selectedIndices);
    const start = updatedPhrases[index].startIndex;
    const stop = updatedPhrases[index].stopIndex;

    for (let i = start; i <= stop; i++) {
      updatedSelectedIndices.delete(i);
    }

    updatedPhrases.splice(index, 1);

    setPhrases(updatedPhrases);
    setSelectedIndices(updatedSelectedIndices);

    if (!updatedPhrases.length) {
      setActivePhraseIndex(-1);
    } else if (index === updatedPhrases.length) {
      setActivePhraseIndex(index - 1);
    }
  }

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
        open={drawerOpen}
        onOpen={() => setDrawerOpen(true)}
        onClose={() => setDrawerOpen(false)}>
          <PhrasesContainer>
            <PhrasesContent
              activePhraseIndex={activePhraseIndex}
              phrases={phrases}
              handleDeletePhrase={handleDeletePhrase} />
          </PhrasesContainer>
      </MobilePhrasesDrawer>
    </>
  );
};

export default Read;
