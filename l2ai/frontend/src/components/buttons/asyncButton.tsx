import React, { useState } from "react";

interface IAsyncButtonProps {
  onClick: () => Promise<any>;
  children: React.ReactNode;
  type: string;
}

const AsyncButton: React.FC<IAsyncButtonProps> = ({ onClick, children, type }) => {
  const [loading, setLoading] = useState<boolean>(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      await onClick();
    } finally {
      setLoading(false);
    }
  };

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
      className={`btn btn-large btn-${type}`}
      onClick={handleClick}
      disabled={loading}
    >
      {loading ? loader : children}
    </button>
  );
};

export default AsyncButton;
