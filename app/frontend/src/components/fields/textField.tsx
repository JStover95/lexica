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

/**
 * TextField component renders an input or textarea element with various
 * configurable properties.
 * 
 * @param {string} [id] - The id attribute for the input or textarea.
 * @param {string} [className] - Additional CSS classes for styling the input or
 *  textarea.
 * @param {string} [type="text"] - The type attribute for the input, can be
 *  "text" or "textarea".
 * @param {string} [placeholder=""] - Placeholder text for the input or
 *  textarea.
 * @param {string} [prefill] - Initial prefilled value for the input or
 *  textarea.
 * @param {string} [value] - Controlled value for the input or textarea.
 * @param {string} [label] - Label text associated with the input or textarea.
 * @param {string} [feedback] - Feedback text to be displayed below the input or
 *  textarea.
 * @param {boolean} [disabled] - If true, disables the input or textarea.
 * @param {Function} [onKeyup] - Callback function triggered on key up event
 *  within the input or textarea.
 * 
 * @returns {JSX.Element} A React component rendering an input or textarea field
 *  with optional label and feedback text.
 */

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
  // State to manage the text value of the input or textarea
  const [text, setText] = useState<string>("");

  // State to manage the visibility of the feedback text
  const [showFeedback, setShowFeedback] = useState<boolean>(true);

  /**
   * Handle change in input or textarea value.
   * 
   * @param {React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>} e -
   *  Event triggered while changing value.
   */
  const handleChange = (
    e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    const inputValue = e.target.value;
    setText(inputValue);

    // Trigger the onKeyup callback with the current input value
    if (onKeyup) onKeyup(inputValue);
  };

  return (
    <React.Fragment>
      {type === "textarea" ? (

        // Render textarea for type "textarea"
        <textarea
          className={"h100p w100p pr1 " + (className ? className : "")}
          placeholder={placeholder}
          defaultValue={prefill}
          value={value}
          onChange={handleChange}
          disabled={disabled}
        ></textarea>
      ) : (

        // Render input for other types
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

      {/* Conditionally render feedback text */}
      {feedback && showFeedback && <span className="font-s font-red">{feedback}</span>}

      {/* Render associated label if provided */}
      {label && (
        <label className="font-s" htmlFor={id}>
          {label}
        </label>
      )}
    </React.Fragment>
  );
};

export default TextField;
