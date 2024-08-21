import React, { useState } from "react";
import "./textField.css";

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

  const handleChange = (
    e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    const inputValue = e.target.value;
    setText(inputValue);
    if (onKeyup) onKeyup(inputValue);
  };

  return (
    <div className="text-field-container">
      {label && (
        <label className="text-field-label" htmlFor={id}>
          {label}
        </label>
      )}
      <div
        className={
          "text-field-content border-light" + (disabled ? " bg-light" : "")
        }
      >
        <div className="text-field-input">
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
      </div>
      {feedback && <span className="text-field-feedback">{feedback}</span>}
    </div>
  );
};

export default TextField;
