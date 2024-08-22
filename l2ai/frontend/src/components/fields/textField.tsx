import React, { useState } from "react";

import "../../styleSheets/styles.css";

interface ITextFieldProps {
  id?: string;
  className?: string;
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
  className,
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
          className={"h100p w100p pr1 " + (className ? className : "")}
          placeholder={placeholder}
          defaultValue={prefill}
          value={value}
          onChange={handleChange}
          disabled={disabled}
        ></textarea>
      ) : (
        <input
          className={"h100p w100p " + (className ? className : "")}
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
