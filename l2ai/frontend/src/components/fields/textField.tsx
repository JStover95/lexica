import * as React from "react";
import { Component } from "react";
import "./textField.css";

/**
 * id (optional): an optional html id
 * type (optional): text, number, date, etc.
 * placeholder (optional): an optional placeholder
 * prefill (optional): a default value (which cannot be changed)
 * value (optional): the field's value (which can be changed)
 * label (optional): the field's label
 * onKeyup (optional): a callback function on keyup
 * feedback (optional): feedback when an error is made
 * disabled (optional): whether to disable the field
 */
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

/**
 * text: the text to display
 */
interface ITextFieldState {
  text: string;
}

class TextField extends React.Component<ITextFieldProps, ITextFieldState> {
  state = { text: "" };

  render() {
    const {
      id,
      type,
      placeholder,
      prefill,
      label,
      feedback,
      disabled,
      value,
      onKeyup
    } = this.props;

    return (
      <div className="text-field-container">

        {/* if a label was passed as a prop */}
        {label ? (
          <label className="text-field-label" htmlFor={id}>{label}</label>
        ) : null}
        <div
          className={
            "text-field-content border-light" + (disabled ? " bg-light" : "")
          }
        >

          {/* TODO: add optional vector icons here */}

          {/* the input */}
          <div className="text-field-input">
            {/* textares require a unique e.target class */}
            {type == "textarea" ? (
              <textarea
                defaultValue={prefill ? prefill : undefined}
                onChange={
                  onKeyup
                    ? (e) => onKeyup((e.target as HTMLTextAreaElement).value)
                    : () => null
                }
              ></textarea>
            ) : (
              <input
                type={type ? type : "text"}
                placeholder={placeholder ? placeholder : ""}
                defaultValue={prefill ? prefill : undefined}
                value={value}
                onChange={
                  onKeyup
                    ? (e) => onKeyup((e.target as HTMLInputElement).value)
                    : () => null
                }
                disabled={disabled}
              />
            )}
          </div>
        </div>

        {/* feedback on error */}
        {feedback ? (
          <span className="text-field-feedback">{feedback}</span>
        ) : null}
      </div>
    );
  }
}

export default TextField;
