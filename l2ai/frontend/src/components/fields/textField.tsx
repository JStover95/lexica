import React, { useState } from "react";

import "../../styleSheets/styles.css";

interface ITextFieldProps {
  id?: string;
  type?: string;
  placeholder?: string;
  prefill?: string;
  value?: string;
  label?: string;
  feedback?: string;
  disabled?: boolean;
  onKeyup?: (text: string) => void;
}

const TextField: React.FC<ITextFieldProps> = ({
  id,
  type = "text",
  placeholder = "",
  prefill,
  value,
  label,
  feedback,
  disabled,
  onKeyup,
}) => {
  const [text, setText] = useState<string>("");
  const [showFeedback, setShowFeedback] = useState<boolean>(true);

  const handleChange = (
    e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    const inputValue = e.target.value;
    setText(inputValue);
    if (onKeyup) onKeyup(inputValue);
  };

  return (
    <React.Fragment>
      {type === "textarea" ? (
        <textarea
          className="hfull wfull"
          placeholder={placeholder}
          defaultValue={prefill}
          value={value}
          onChange={handleChange}
          disabled={disabled}
        ></textarea>
      ) : (
        <input
          className="hfull wfull"
          type={type}
          placeholder={placeholder}
          defaultValue={prefill}
          value={value}
          onChange={handleChange}
          disabled={disabled}
        />
      )}
      {feedback && showFeedback && <span className="font-s font-red">{feedback}</span>}
      {label && (
        <label className="font-s" htmlFor={id}>
          {label}
        </label>
      )}
    </React.Fragment>
  );
};

export default TextField;
