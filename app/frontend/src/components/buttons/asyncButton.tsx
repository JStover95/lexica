import React, { useState } from "react";

interface IAsyncButtonProps {
  onClick: () => Promise<any>;
  children: React.ReactNode;
  type: string;
  size: string;
}

/**
 * `AsyncButton` is a React functional component that renders a button that,
 * when clicked, executes an asynchronous function and provides visual feedback
 * (via a loading spinner) until the function resolves.
 *
 * Props:
 * @param {() => Promise<any>} onClick - Function to be called when the button
 *  is clicked. Should return a Promise.
 * @param {React.ReactNode} children - The content to be displayed within the
 *  button.
 * @param {string} type - The CSS class modifier for the button's type.
 * @param {string} size - The CSS class modifier for the button's size.
 *
 * @returns {JSX.Element} A button element which displays a loading spinner
 *  while the asynchronous function is executing.
 */
const AsyncButton: React.FC<IAsyncButtonProps> = ({ onClick, children, type, size }) => {
  // State to manage the loading state of the button
  const [loading, setLoading] = useState<boolean>(false);

  // Set the loading state, call the passed onClick function, and reset the loading state
  const handleClick = async () => {
    setLoading(true);
    try {
      await onClick();
    } finally {
      setLoading(false);
    }
  };

  // Loader JSX element to be shown when the button is in the loading state
  const loader = (
    <div className="lds-ring lds-ring-small">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  );

  return (
    <button
      className={`btn btn-${size} btn-${type}`}
      onClick={handleClick}
      disabled={loading} // Disable the button when it is in the loading state
    >
      {/* Show loader if loading, else show children */}
      {loading ? loader : children}
    </button>
  );
};

export default AsyncButton;
