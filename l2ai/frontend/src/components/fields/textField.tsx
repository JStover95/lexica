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
    <div>
      <div
        className={
          (disabled ? "border-mid bg-light" : "border-b-mid")
        }
      >
        {type === "textarea" ? (
          <textarea
            defaultValue={prefill}
            onChange={handleChange}
            disabled={disabled}
          ></textarea>
        ) : (
          <input
            type={type}
            placeholder={placeholder}
            defaultValue={prefill}
            value={value}
            onChange={handleChange}
            disabled={disabled}
          />
        )}
      </div>
      {feedback && showFeedback && <span className="font-s font-red">{feedback}</span>}
      {label && (
        <label className="font-s" htmlFor={id}>
          {label}
        </label>
      )}
    </div>
  );
};

export default TextField;
